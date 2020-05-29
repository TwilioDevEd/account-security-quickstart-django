from django.conf import settings
from django.test import TestCase, Client
try:
    from unittest.mock import patch, MagicMock, Mock
except ImportError:
    from mock import patch, MagicMock

from . import views
from .forms import VerificationForm

class MockVerificationForm:
    cleaned_data = {"phone_number": "+593999999999", "via": "SMS"}

    def is_valid(self):
        return True

class MockTokenForm:
    cleaned_data = {"phone_number": "+593999999999", "via": "SMS", "token":"token"}

    def is_valid(self):
        return True

    def add_error(self, param1, param2):
        return "added error"

class MockVerification:
    def __init__(self, status_value):
        self.status = status_value

    def errors(self):
        return MockErrorValues()

class MockErrorValues:
    def values(self):
        return "error"

class PhoneVerificationTestCase(TestCase):

    @patch('phone_verification.views.twilio_client.verifications', return_value='mock verifications!')
    @patch('phone_verification.views.VerificationForm', return_value=MockVerificationForm())
    def test_phone_verification_redirects_to_token_validation(self, mock_verification_form, mock_twilio_client):
        client = Client()

        response = client.post('/verification/')

        mock_twilio_client.assert_called_with('+593999999999', "SMS")
        assert response.status_code == 302
        assert '/verification/token/' in response.url

    def test_phone_verification_render_phone_verification_for_different_method(self):
        client = Client()

        response = client.get('/verification/')
        self.assertTemplateUsed(response, 'phone_verification.html')

    @patch('phone_verification.views.twilio_client.verification_checks', return_value=MockVerification("approved"))
    @patch('phone_verification.views.TokenForm', return_value=MockTokenForm())
    def test_token_validation_redirects_to_verified_when_status_not_approved(self, mock_token_form, mock_twilio_client):
        client = Client()
        session = client.session
        session['phone_number'] = "1234"
        session.save()

        response = client.post('/verification/token/')

        assert client.session['is_verified'] == True
        assert response.status_code == 302
        assert '/verified/' in response.url

    @patch('phone_verification.views.twilio_client.verification_checks', return_value=MockVerification("pending"))
    @patch('phone_verification.views.TokenForm', return_value=MockTokenForm())
    def test_token_validation_error_when_status_not_approved(self, mock_token_form, mock_twilio_client):
        client = Client()
        session = client.session
        session['phone_number'] = "1234"
        session.save()

        response = client.post('/verification/token/')
        mock_twilio_client.assert_called()
        self.assertTemplateUsed(response, 'token_validation.html')

    def test_token_validation_render_phone_verification_for_different_method(self):
        client = Client()

        response = client.get('/verification/')
        self.assertTemplateUsed(response, 'phone_verification.html')
