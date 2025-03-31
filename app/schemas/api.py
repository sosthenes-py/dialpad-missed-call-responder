from pydantic import BaseModel


class CallEventResponseSchema(BaseModel):
    hook_id: int
    event_id: int