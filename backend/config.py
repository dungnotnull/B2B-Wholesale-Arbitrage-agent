import os
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # API Keys
    google_vision_api_key: str = os.getenv("GOOGLE_VISION_API_KEY", "")
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    azure_vision_key: str = os.getenv("AZURE_VISION_KEY", "")
    azure_vision_endpoint: str = os.getenv("AZURE_VISION_ENDPOINT", "")
    deepl_api_key: str = os.getenv("DEEPL_API_KEY", "")

    # DB & Infrastructure
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/wholesale_arbitrage.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # ML Models
    clip_model_id: str = os.getenv("CLIP_MODEL_ID", "openai/clip-vit-large-patch14")
    translation_zh_en: str = os.getenv("OFFLINE_TRANSLATION_MODEL_ZH_EN", "Helsinki-NLP/opus-mt-zh-en")
    translation_en_zh: str = os.getenv("OFFLINE_TRANSLATION_MODEL_EN_ZH", "Helsinki-NLP/opus-mt-en-zh")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    # Platforms
    url_1688: str = os.getenv("PLATFORM_1688_BASE_URL", "https://1688.com")
    url_alibaba: str = os.getenv("PLATFORM_ALIBABA_BASE_URL", "https://alibaba.com")

    class Config:
        env_file = ".env"

settings = Settings()
