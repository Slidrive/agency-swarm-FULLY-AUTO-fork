from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from .agency import build_agency
from .settings import ProductionSettings


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None


class ChatResponse(BaseModel):
    thread_id: str
    output: str


def _get_settings() -> ProductionSettings:
    return ProductionSettings()


def _get_agency(settings: ProductionSettings = Depends(_get_settings)):
    return build_agency(settings)


def _auth(settings: ProductionSettings, api_key: str | None) -> None:
    expected_header = settings.api_key_header
    # If no API key is set in environment, allow open access. Otherwise enforce header.
    # Set e.g. AGENCY_API_KEY_HEADER=X-API-Key and send that header with your key.
    expected_value = None
    # If the user defines AGENCY_API_KEY_<anything> we could add enforcement; keeping minimal here.
    # For now, only check presence if env var "AGENCY_CLIENT_API_KEY" exists.
    import os

    client_key = os.getenv("AGENCY_CLIENT_API_KEY")
    if client_key:
        if not api_key or api_key != client_key:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
    # else: open access


app = FastAPI(title="Agency Swarm Production API", version="1.0.0")


@app.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    settings: ProductionSettings = Depends(_get_settings),
    agency=Depends(_get_agency),
    api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    _auth(settings, api_key)
    # Use CEO entry point (first entry agent)
    entry = agency.entry_points[0]
    result = await agency.get_response(message=payload.message, entry_point=entry, thread_id=payload.thread_id)
    return ChatResponse(thread_id=result.thread_id, output=result.final_output)


__all__ = ["app"]
