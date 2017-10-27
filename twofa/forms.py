import phonenumbers

from authy.api import AuthyApiClient
from django import forms
from django.conf import settings
from phonenumbers.phonenumberutil import NumberParseException

from .models import TwoFAUser


authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


class BootstrapInput(forms.TextInput):
    def __init__(self, placeholder, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapInput, self).__init__(attrs={
            'class': 'form-control input-sm',
            'placeholder': placeholder
        })

    def bootwrap_input(self, input_tag):
        size_classes = 'col-xs-{col} col-sm-{col} col-md-{col}'.format(col=self.size)

        return '''<div class="{size}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(size=size_classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapInput, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class BootstrapPasswordInput(BootstrapInput):
    input_type = 'password'
    template_name = 'django/forms/widgets/password.html'


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = TwoFAUser
        fields = ('username', 'email', 'password')
        widgets = {
            'username': BootstrapInput('User Name'),
            'email': BootstrapInput('Email Address'),
            'password': BootstrapPasswordInput('Password', size=6),
        }

    country_code = forms.CharField(widget=BootstrapInput('Country Code', size=6))
    phone_number = forms.CharField(widget=BootstrapInput('Phone Number', size=6))
    confirm_password = forms.CharField(widget=BootstrapPasswordInput('Confirm Password', size=6))

    def clean_username(self):
        username = self.cleaned_data['username']
        if TwoFAUser.objects.filter(username=username).exists():
            self.add_error('username', 'Username is already taken')
        return username

    def clean_country_code(self):
        country_code = self.cleaned_data['country_code']
        if not country_code.startswith('+'):
            country_code = '+' + country_code
        return country_code

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('password', 'Password and confirmation did not match')
        phone_number = self.cleaned_data['country_code'] + self.cleaned_data['phone_number']
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Invalid phone number')
        except NumberParseException as e:
            self.add_error('phone_number', e)


class TokenVerificationForm(forms.Form):
    token = forms.CharField(
        required=True,
        widget=BootstrapInput('Token via SMS, Voice or SoftToken')
    )

    def is_valid(self, authy_id):
        self.authy_id = authy_id
        return super(TokenVerificationForm, self).is_valid()

    def clean(self):
        token = self.cleaned_data['token']
        verification = authy_api.tokens.verify(self.authy_id, token)
        if not verification.ok():
            self.add_error('token', 'Invalid token')
