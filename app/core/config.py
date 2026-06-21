from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PROJECT_NAME is the human-readable name of the application.
    # Keeping it in settings makes it easy to change later from the .env file.
    PROJECT_NAME: str = "AI Shopping Assistant Backend"

    # API_V1_PREFIX is the common prefix for version 1 API routes.
    # This helps keep routes organized as the project grows.
    API_V1_PREFIX: str = "/api/v1"

    # DATABASE_URL tells SQLAlchemy which database to connect to.
    # For Phase 1, we use a local SQLite database file.
    DATABASE_URL: str = "sqlite:///./shopping_assistant.db"

    # model_config tells pydantic-settings to read values from a .env file.
    # If a value exists in .env, it can override the default above.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# This is the settings object the rest of the project will import.
# It loads configuration one time when the app starts.
settings = Settings()
