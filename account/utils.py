from django.conf import settings
from twilio.rest import Client

account_sid = settings.TWILIO_ACCOUNT_SID
account_token = settings.TWILIO_AUTH_TOKEN
twilio_sender = settings.TWILIO_SENDER_PHONE


def send_activation_sms(phone_number, activation_code):
    message = f'Hi! This is your activation code: {activation_code}.'
    client = Client(account_sid, account_token)
    client.messages.create(
        body=message,
        from_=twilio_sender,
        to=phone_number
    )
