from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProductionSettings(BaseSettings):
    """Environment-driven settings for a production agency deployment."""

    model_config = SettingsConfigDict(env_prefix="AGENCY_", case_sensitive=False)

    agency_name: str = Field(default="Production Agency")
    model: str = Field(default="gpt-5")
    max_active_tasks_per_agent: int = Field(default=3)

    # API/auth
    api_key_header: str = Field(default="X-API-Key")

    # External service placeholders (wire real endpoints/keys in your environment)
    genesis_api_base: str | None = None
    genesis_api_key: str | None = None
    voice_api_base: str | None = None
    voice_api_key: str | None = None
