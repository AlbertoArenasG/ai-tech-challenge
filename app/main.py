"""FastAPI application entry point."""
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.domain.schemas import ChatRequest, ChatResponse
from app.services.agent_service import CommercialAgentService
from app.services.catalog_service import CatalogService

LOGGER = logging.getLogger(__name__)

app = FastAPI(title="Kavak Commercial Bot")
settings = get_settings()
catalog_service = CatalogService()
agent_service = CommercialAgentService(
    catalog_service=catalog_service,
    settings=settings,
    knowledge_base_path=settings.value_proposition_path,
)


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


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """Route inbound chat messages through the commercial agent."""
    try:
        return agent_service.answer(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
