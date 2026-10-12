from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    tg_bot_token: str
    db_url: str
    model_name: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

SETTINGS = Settings()