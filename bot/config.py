from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    BACKEND_URL: str = "http://localhost:8000"
    CRYPTOBOT_TOKEN: str

    class Config:
        env_file = "backend/.env"
        extra = "ignore"

settings = Settings()

