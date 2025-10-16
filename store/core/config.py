from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Store API"
    ROOT_PATH: str = "/"

    # Database Configuration
    DATABASE_URL: str
    DATABASE_NAME: str = "store"

    # MongoDB Configuration (optional fields used by Docker)
    MONGODB_REPLICA_SET_MODE: str = "primary"
    MONGODB_ADVERTISED_HOSTNAME: str = "localhost"
    ALLOW_EMPTY_PASSWORD: str = "yes"

    # Application Configuration (optional fields)
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    APP_RELOAD: bool = True

    # Docker Configuration (optional field)
    COMPOSE_PROJECT_NAME: str = "store-api"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
