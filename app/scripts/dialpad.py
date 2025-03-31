from app.services.dialpad import CallEventApi
from decouple import config


DIALPAD_SECRET = config('DIALPAD_SECRET')

# create event
call_event = CallEventApi(event='missed')
created, message = call_event.create(webhook_url='', secret=DIALPAD_SECRET)
print({
    'created': created,
    'message': message,
    **call_event.response
})
