from pydantic import BaseModel


class WebhookSignatureSchema(BaseModel):
    algo: str
    secret: str
    type: str


class WebhookSchema(BaseModel):
    hook_url: str
    id: int
    signature: WebhookSignatureSchema


class ContactSchema(BaseModel):
    phone: str
    type: str
    id: str
    name: str


class MissedCallEventSchema(BaseModel):
    date_ended: int
    internal_number: str
    duration: float
    total_duration: float
    call_id: int
    state: str
    direction: str
    contact: ContactSchema

