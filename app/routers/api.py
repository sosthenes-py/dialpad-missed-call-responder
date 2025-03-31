from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.dialpad import CallEventApi
from decouple import config


DIALPAD_SECRET = config('DIALPAD_SECRET')

router = APIRouter()

@router.get('/create-event')
async def create():
    call_event = CallEventApi(event='missed')
    code, created, message = call_event.create(webhook_url='', secret=DIALPAD_SECRET)
    return JSONResponse(
        {'created': created, 'message': message, 'hook_id': call_event.hook_id, 'event_id': call_event.event_id}, code)

