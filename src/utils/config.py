"""Configuration loading for the copilot application.

Why this exists:
    Production-oriented apps should not hard-code secrets, model names, or
    storage paths throughout the codebase. A central settings object makes the
    system easier to deploy locally, on Streamlit Community Cloud, and later in
    more advanced environments.
"""

from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "configs" / "app_config.yaml"


class Settings(BaseSettings):
    """Environment variables used by the application."""

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_persist_dir: str = "data/vector_store"
    sqlite_db_path: str = "data/sqlite/copilot.db"
    sec_user_agent: str = "FinanceSupplyChainCopilot contact@example.com"
    app_env: str = "development"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def load_yaml_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load non-secret application defaults from YAML."""

    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def get_settings() -> Settings:
    """Load .env values and return a typed settings object."""

    load_dotenv(PROJECT_ROOT / ".env")
    return Settings()
