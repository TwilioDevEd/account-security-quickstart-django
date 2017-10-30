from django.conf import settings
from django.test import TestCase, Client
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

from . import views
from .models import TwoFAUser


class TwoFATestCase(TestCase):
    def test_protected_redirect_anonymous_to_login(self):
        # Arrange
        client = Client()

        # Act
        response = client.get('/protected/')

        # Assert
        self.assertRedirects(
            response,
            settings.LOGIN_URL,
            fetch_redirect_response=False
        )

    def test_protected_logged_in_user_redirected_to_2fa(self):
        # Arrange
        TwoFAUser.objects.create_user(
            username='test',
            authy_id='fake',
            password='test'
        )
        client = Client()
        client.login(username='test', password='test')

        # Act
        response = client.get('/protected/')

        # Assert
        self.assertRedirects(response, '/2fa/', fetch_redirect_response=False)

    def test_protected_displays_to_authy_user(self):
        # Arrange
        TwoFAUser.objects.create_user(
            username='test',
            authy_id='fake',
            password='test'
        )
        client = Client()
        client.login(username='test', password='test')
        session = client.session
        session['authy'] = True
        session.save()

        # Act
        response = client.get('/protected/', follow=True)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, views.protected)

    @patch('twofa.views.authy_api')
    def test_token_sms_success(self, authy_api):
        # Arrange
        TwoFAUser.objects.create_user(
            username='test',
            authy_id='fake',
            password='test'
        )
        client = Client()
        client.login(username='test', password='test')

        request_sms_response = MagicMock()
        request_sms_response.ok.return_value = True
        authy_api.users.request_sms.return_value = request_sms_response

        # Act
        response = client.post('/token/sms')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, views.token_sms)
        authy_api.users.request_sms.assert_called_once_with(
            'fake',
            {'force': True}
        )
        request_sms_response.ok.assert_called_once()

    @patch('twofa.views.authy_api')
    def test_token_sms_failure(self, authy_api):
        # Arrange
        TwoFAUser.objects.create_user(
            username='test',
            authy_id='fake',
            password='test'
        )
        client = Client()
        client.login(username='test', password='test')

        request_sms_response = MagicMock()
        request_sms_response.ok.return_value = False
        authy_api.users.request_sms.return_value = request_sms_response

        # Act
        response = client.post('/token/sms')

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.resolver_match.func, views.token_sms)
        authy_api.users.request_sms.assert_called_once_with(
            'fake',
            {'force': True}
        )
        request_sms_response.ok.assert_called_once()
