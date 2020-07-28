from pydantic import BaseSettings


class Settings(BaseSettings):
    PASSWORD_MIN_LENGTH: int = 10
    ACCESS_TOKEN_EXPIRATION: int = 30
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str
    DB_URL: str = "sqlite:///./app.db"
    DB_TYPE: str = "SQLite"
    TESTING: bool = False
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str


settings = Settings()
