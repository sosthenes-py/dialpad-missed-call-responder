import requests
from decouple import config
from typing import Optional

from app.schemas.webhook import MissedCallEventSchema
import jwt
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, InvalidTokenError
import aiohttp

import logging


BASE_URL = 'https://dialpad.com/api/v2'
DIALPAD_KEY = config('DIALPAD_API_KEY')
SECRET = config('DIALPAD_SECRET')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_webhook(event: MissedCallEventSchema):
    sent = await send_sms(
                event.internal_number,
                event.contact.phone,
                config('SMS_MESSAGE'),
                event.internal_number
            )
    if sent:
        return JSONResponse({'status': 'ok'}, status_code=200)
    return JSONResponse({'status': 'error'}, status_code=501)

async def verify_signature(request):
    payload = await request.body()
    try:
        decoded_payload = jwt.decode(payload, SECRET, algorithms=["HS256"])
        return MissedCallEventSchema(**decoded_payload)
    except ExpiredSignatureError:
        logger.info('Webhook Signature expired.')
        return None
    except InvalidTokenError:
        logger.info('Webhook Token Invalid.')
        return None

async def send_sms(from_number, to_number, text, user_id):
    api_url = BASE_URL + "/sms"

    payload = {
        "infer_country_code": False,
        "from_number": from_number,
        "text": text,
        "to_numbers": [to_number],
        "user_id": user_id
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {DIALPAD_KEY}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                logger.info(f'SMS sending failed: {response.text()}')
                return None
    except Exception as e:
        logger.info(f'SMS sending failed: {str(e)}')

def create_webhook(url, secret):
    api_url = "https://dialpad.com/api/v2/webhooks"

    payload = {
        "hook_url": url,
        "secret": secret
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {DIALPAD_KEY}"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating webhook: {e}")
        return None
    else:
        if response.status_code == 200:
            return response.json()
        logger.error(f"Error creating webhook: {response.text}")
        return response.text




class CallEventApi:
    def __init__(self, event):
        self.event = event
        self.hook_id = None
        self.event_id = None

    def create(self, webhook_url, secret):
        try:
            webhook = create_webhook(webhook_url, secret)
            if webhook is not None and not isinstance(webhook, str):
                self.hook_id = webhook.get('id')
                created_event = self._create_subscription()
                if created_event:
                    self.event_id = created_event['id']
                    return 200, True, 'success'
                return 403, False, 'Event creation failed'
            return 403, False, 'Webhook creation failed'
        except Exception as e:
            logger.info(f'Failed to create webhook: {e}')
            return 403, False, str(e)

    def _get_subscriptions(self):
        endpoint = '/subscriptions/call'
        response = self._send_request('get', endpoint)
        if response and response.status_code == 200:
            return response.json()
        return None

    def _create_subscription(self):
        endpoint = '/subscriptions/call'
        payload = {
            "enabled": True,
            "call_states": [self.event],
            "endpoint_id": self.hook_id
        }
        response = self._send_request('post', endpoint, json=payload)
        if response and response.status_code == 200:
            return response.json()
        return None

    def _send_request(self, method, endpoint, **kwargs):
        url = f'{BASE_URL}{endpoint}'
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {DIALPAD_KEY}'
        }
        try:
            response =  requests.request(method=method, url=url, headers=headers, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.info(e)
            return None
        else:
            return response
