from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "EduGenie"

    gemini_api_key: str = ""

    # You can change this model in .env if needed.
    gemini_model: str = "gemini-3.8-flash"

    # Optional local explanation model
    use_local_explainer: bool = False

    local_explainer_model: str = (
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    max_input_chars: int = 12000

    request_timeout_seconds: int = 90

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()