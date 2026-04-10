from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ALCHEMIES_", extra="ignore")

    env: str = "development"
    app_name: str = "Alchemies API"
    public_base_url: str = Field(default="http://127.0.0.1:8000")


settings = Settings()
