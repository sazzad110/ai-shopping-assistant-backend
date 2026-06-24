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

    # GROQ_API_KEY is used by the AI chat endpoint.
    # It is intentionally optional so the rest of the app can still run without it.
    GROQ_API_KEY: str = ""

    # GROQ_MODEL selects which Groq-hosted model the chat assistant uses.
    GROQ_MODEL: str = "qwen/qwen3-32b"

    # AI_AGENT_ENABLED makes it easy to turn the chat endpoint on or off.
    AI_AGENT_ENABLED: bool = True

    # model_config tells pydantic-settings to read values from a .env file.
    # If a value exists in .env, it can override the default above.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# This is the settings object the rest of the project will import.
# It loads configuration one time when the app starts.
settings = Settings()
