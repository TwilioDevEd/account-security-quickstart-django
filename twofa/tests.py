from django.conf import settings
from django.test import TestCase, Client

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
        self.assertEqual(response.resolver_match.func, views.protected)
