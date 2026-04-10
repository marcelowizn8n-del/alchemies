from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ALCHEMIES_", extra="ignore")

    env: str = "development"
    app_name: str = "Alchemies API"
    public_base_url: str = Field(default="http://127.0.0.1:8010")
    cors_allow_origins: str = Field(default="*")

    @property
    def cors_origins(self) -> list[str]:
        if self.cors_allow_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


settings = Settings()
