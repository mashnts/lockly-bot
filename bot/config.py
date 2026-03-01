from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    BACKEND_URL: str = "https://lockly-bot-5.onrender.com"
    CRYPTOBOT_TOKEN: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()