from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.agent.prompts import SHOPPING_ASSISTANT_SYSTEM_PROMPT
from app.agent.tools import create_shopping_tools
from app.core.config import settings


def create_shopping_agent(db: Session):
    # The agent is created per request so it can use the current DB session
    # and so missing API keys do not break app startup.
    if not settings.AI_AGENT_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="AI agent is disabled",
        )

    if not settings.GROQ_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GROQ_API_KEY is not configured",
        )

    from langchain_groq import ChatGroq

    tools = create_shopping_tools(db)
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=0,
    )
    return llm.bind_tools(tools), {tool.name: tool for tool in tools}


def _convert_history_to_messages(history: Optional[list[dict]]):
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    messages = [SystemMessage(content=SHOPPING_ASSISTANT_SYSTEM_PROMPT)]

    for item in history or []:
        role = item.get("role", "user")
        content = item.get("content", "")

        if role == "assistant":
            messages.append(AIMessage(content=content))
        elif role == "system":
            messages.append(SystemMessage(content=content))
        else:
            messages.append(HumanMessage(content=content))

    return messages


def _extract_text_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(content)


def run_shopping_agent(
    db: Session,
    message: str,
    history: Optional[list[dict]] = None,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
) -> str:
    # The flow is:
    # 1. Create the model and tools for this request.
    # 2. Convert prior chat history into LangChain message objects.
    # 3. Add the current user message.
    # 4. Run a small tool-calling loop until the assistant returns final text.
    from langchain_core.messages import HumanMessage, ToolMessage

    model_with_tools, tool_map = create_shopping_agent(db)
    messages = _convert_history_to_messages(history)

    user_message = message.strip()
    if customer_name or customer_email:
        user_message += "\n\nAvailable checkout details:"
        if customer_name:
            user_message += f"\nCustomer name: {customer_name}"
        if customer_email:
            user_message += f"\nCustomer email: {customer_email}"

    messages.append(HumanMessage(content=user_message))

    for _ in range(5):
        ai_message = model_with_tools.invoke(messages)
        messages.append(ai_message)

        tool_calls = getattr(ai_message, "tool_calls", None) or []
        if not tool_calls:
            final_text = _extract_text_content(ai_message.content)
            return final_text or "I could not generate a response."

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            tool_result = tool_map[tool_name].invoke(tool_args)
            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                    name=tool_name,
                )
            )

    return "I could not finish the shopping request. Please try again with a simpler message."
