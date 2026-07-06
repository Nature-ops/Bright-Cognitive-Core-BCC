from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Bright Assistant"
    VERSION: str = "0.2.0"
    DEBUG: bool =True

    class Config:
        env_file = ".env"
        case_sensitive =True


settings = Settings()