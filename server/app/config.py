from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 9000
    api_token: str | None = None
    enable_control: bool = False

    model_config = SettingsConfigDict(
        env_prefix="AI_CONTROL_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
