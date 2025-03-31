from fastapi import APIRouter, Request
from app.services.dialpad import handle_webhook, verify_signature
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post('/webhook')
async def webhook(request: Request):
    event = await verify_signature(request)
    if event:
        return await handle_webhook(event)
