from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str
    CRYPTOBOT_TOKEN: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
