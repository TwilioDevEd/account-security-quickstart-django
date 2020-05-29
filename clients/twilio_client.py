from twilio.rest import Client
from django.conf import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def verifications(phone_number, via):
        return client.verify \
                    .services(settings.TWILIO_VERIFICATION_SID) \
                    .verifications \
                    .create(to=phone_number, channel=via)

def verification_checks(phone_number, token):
        return client.verify \
                    .services(settings.TWILIO_VERIFICATION_SID) \
                    .verification_checks \
                    .create(to=phone_number, code=token)
