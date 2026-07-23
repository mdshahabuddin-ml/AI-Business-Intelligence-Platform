from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 60
    upload_dir: str = "storage/uploads"
    processed_dir: str = "storage/processed"

    class Config:
        env_file = ".env"


settings = Settings()