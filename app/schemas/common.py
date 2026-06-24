from pydantic import BaseModel


class MessageResponse(BaseModel):
    # This simple schema is used for success messages,
    # especially for delete endpoints.
    message: str
