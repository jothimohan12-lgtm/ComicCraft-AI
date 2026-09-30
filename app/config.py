from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str | None = None

    hf_token: str | None = None

    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-flash"

    hf_image_model: str = "stabilityai/stable-diffusion-xl-base-1.0"

    image_provider: str = "placeholder"

    local_image_model: str = "runwayml/stable-diffusion-v1-5"
    local_image_device: str = "auto"
    local_image_steps: int = 25

    panel_count: int = 5
    max_prompt_length: int = 2000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()