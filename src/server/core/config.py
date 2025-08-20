from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AMMUT_HOST: str = "0.0.0.0"
    AMMUT_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
