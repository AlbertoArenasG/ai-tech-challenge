"""FastAPI application entry point."""
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import PlainTextResponse
from redis.exceptions import RedisError

from app.config import get_settings
from app.domain.schemas import ChatRequest, ChatResponse
from app.adapters.whatsapp_adapter import format_twilio_response, parse_twilio_payload
from app.services.agent_service import CommercialAgentService
from app.services.catalog_service import CatalogService
from app.services.message_parser import MessageParser
from app.services.conversation_store import ConversationStore
from app.services.intent_classifier import IntentClassifier
from app.services.option_builder import OptionBuilder

LOGGER = logging.getLogger(__name__)

app = FastAPI(title="Kavak Commercial Bot")
settings = get_settings()
catalog_service = CatalogService()
agent_service = CommercialAgentService(
    catalog_service=catalog_service,
    settings=settings,
    knowledge_base_path=settings.value_proposition_path,
)
message_parser = MessageParser(catalog_service)
conversation_store = ConversationStore(settings.redis_url)
intent_classifier = IntentClassifier(settings.openai_api_key, settings.openai_model)
option_builder = OptionBuilder(catalog_service)


def _safe_get_preferences(user_id: str) -> dict:
    try:
        return conversation_store.get_preferences(user_id)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when getting preferences: %s", exc)
        return {}


def _safe_store_preferences(user_id: str, preferences: dict) -> None:
    try:
        conversation_store.store_preferences(user_id, preferences)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when storing preferences: %s", exc)


def _safe_save_turn(user_id: str, payload: dict) -> None:
    try:
        conversation_store.save_turn(user_id, payload)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when saving turn: %s", exc)


def _safe_get_question(user_id: str) -> dict | None:
    try:
        return conversation_store.get_question(user_id)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when getting question: %s", exc)
        return None


def _safe_set_question(user_id: str, slot: str, options: list[str]) -> None:
    try:
        conversation_store.set_question(user_id, slot, options)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when setting question: %s", exc)


def _safe_clear_question(user_id: str) -> None:
    try:
        conversation_store.clear_question(user_id)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when clearing question: %s", exc)


def _safe_get_expected_slot(user_id: str) -> str | None:
    try:
        return conversation_store.get_expected_slot(user_id)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when getting expected slot: %s", exc)
        return None


def _safe_set_expected_slot(user_id: str, slot: str | None) -> None:
    try:
        conversation_store.set_expected_slot(user_id, slot)
    except RedisError as exc:
        LOGGER.warning("Redis unavailable when setting expected slot: %s", exc)


@app.on_event("startup")
async def load_catalog() -> None:
    if not settings.csv_catalog_path:
        LOGGER.warning("CSV_CATALOG_PATH not configured; catalog endpoints will return empty datasets.")
        return

    catalog_path = Path(settings.csv_catalog_path)
    try:
        catalog_service.load_catalog(str(catalog_path))
        LOGGER.info("Catalog loaded from %s", catalog_path)
    except FileNotFoundError as exc:
        LOGGER.error("Catalog file missing: %s", exc)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


def _handle_chat(payload: ChatRequest) -> ChatResponse:
    stored_preferences = _safe_get_preferences(payload.user_id)
    if stored_preferences and not payload.preferences:
        payload.preferences = stored_preferences

    parsed_request = message_parser.enrich_request(payload)

    question = _safe_get_question(payload.user_id)
    if question and question.get("options"):
        slot = question["slot"]
        parsed_prefs = parsed_request.preferences or {}
        satisfied = (
            (slot == "marca" and parsed_prefs.get("make"))
            or (slot == "modelo" and parsed_prefs.get("model"))
        )

        if satisfied:
            _safe_clear_question(payload.user_id)
        else:
            normalized = payload.message.strip().lower()
            normalized_options = {opt.lower(): opt for opt in question["options"]}
            if normalized not in normalized_options:
                formatted = "\n".join(f"- {opt}" for opt in question["options"])
                return ChatResponse(
                    message=(
                        "Para continuar, selecciona una opción de la lista anterior. "
                        "Escribe exactamente uno de los siguientes valores:\n" + formatted
                    ),
                    recommendations=[],
                    financing_plan=None,
                )
            selected = normalized_options[normalized]
            payload.preferences = payload.preferences or {}
            if slot == "marca":
                payload.preferences["make"] = selected
            elif slot == "modelo":
                payload.preferences["model"] = selected
            _safe_clear_question(payload.user_id)
            parsed_request = message_parser.enrich_request(payload)

    enriched_payload = parsed_request
    if enriched_payload.preferences:
        _safe_store_preferences(payload.user_id, enriched_payload.preferences)
    _safe_save_turn(payload.user_id, enriched_payload.model_dump())
    missing_fields = message_parser.identify_missing_fields(payload, enriched_payload)
    expected_slot = _safe_get_expected_slot(payload.user_id)
    intent = intent_classifier.classify(payload.message)

    slot_options = None
    if intent == "greeting":
        _safe_set_expected_slot(payload.user_id, "preferencia_inicial")
    elif intent == "recommendation" and missing_fields:
        _safe_set_expected_slot(payload.user_id, missing_fields[0])
        next_slot = missing_fields[0]
        if next_slot == "marca":
            options = option_builder.make_options()
            _safe_set_question(payload.user_id, "marca", options)
            slot_options = {"slot": "marca", "options": options}
        elif next_slot == "modelo" and enriched_payload.preferences and enriched_payload.preferences.get("make"):
            options = option_builder.model_options(enriched_payload.preferences["make"])
            if options:
                _safe_set_question(payload.user_id, "modelo", options)
                slot_options = {"slot": "modelo", "options": options}
    else:
        _safe_set_expected_slot(payload.user_id, None)
        _safe_clear_question(payload.user_id)

    try:
        return agent_service.answer(
            enriched_payload,
            missing_fields=missing_fields,
            intent=intent,
            expected_slot=expected_slot,
            slot_options=slot_options,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """Route inbound chat messages through the commercial agent."""
    return _handle_chat(payload)

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request) -> PlainTextResponse:
    form = await request.form()
    chat_request = parse_twilio_payload(dict(form))
    response = _handle_chat(chat_request)
    return PlainTextResponse(content=format_twilio_response(response))
