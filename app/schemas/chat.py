from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    # This schema represents one previous chat message
    # shared between the client and the assistant.
    role: str
    content: str


class ChatRequest(BaseModel):
    # This schema is used when the client sends a chat request
    # to the AI shopping assistant.
    message: str = Field(..., min_length=1)
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    history: list[ChatMessage] = Field(default_factory=list)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        # The main user message should not be empty or only whitespace.
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("message cannot be empty")
        return cleaned_value


class ChatResponse(BaseModel):
    # This schema returns the final plain-text reply
    # from the AI assistant.
    reply: str
