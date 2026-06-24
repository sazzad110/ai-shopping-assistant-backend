from sqlalchemy.orm import Session

from app.agent.shopping_agent import run_shopping_agent
from app.schemas.chat import ChatRequest, ChatResponse


def chat_with_agent(db: Session, chat_request: ChatRequest) -> ChatResponse:
    # This service keeps the route thin and acts as the bridge
    # between FastAPI and the LangChain shopping agent.
    reply = run_shopping_agent(
        db=db,
        message=chat_request.message,
        history=[message.model_dump() for message in chat_request.history],
        customer_name=chat_request.customer_name,
        customer_email=chat_request.customer_email,
    )
    return ChatResponse(reply=reply)
