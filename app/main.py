"""FastAPI application entry point."""
from fastapi import FastAPI

from app.config import get_settings
from app.services.agent_service import CommercialAgentService

app = FastAPI(title="Kavak Commercial Bot")
settings = get_settings()
agent_service = CommercialAgentService()


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/chat")
async def chat_endpoint(payload: dict) -> dict:
    """TODO: Formalize payload schema and connect to the conversation workflow."""
    # TODO: Replace the adhoc dict with typed models and orchestrate the agent pipeline.
    _ = payload
    return {"message": agent_service.answer("stub")}
