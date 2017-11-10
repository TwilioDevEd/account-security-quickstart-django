import phonenumbers

from django import forms
from phonenumbers import NumberParseException
from twofa.forms import BootstrapInput


class BootstrapSelect(forms.Select):
    def __init__(self, size=12, *args, **kwargs):
        self.size = size
        super(BootstrapSelect, self).__init__(attrs={
            'class': 'form-control input-sm',
        })

    def bootwrap_input(self, input_tag):
        classes = 'col-xs-{n} col-sm-{n} col-md-{n}'.format(n=self.size)

        return '''<div class="{classes}">
                    <div class="form-group">{input_tag}</div>
                  </div>
               '''.format(classes=classes, input_tag=input_tag)

    def render(self, *args, **kwargs):
        input_tag = super(BootstrapSelect, self).render(*args, **kwargs)
        return self.bootwrap_input(input_tag)


class VerificationForm(forms.Form):
    country_code = forms.CharField(
        widget=BootstrapInput('Country Code', size=3))
    phone_number = forms.CharField(
        widget=BootstrapInput('Phone Number', size=6))
    via = forms.ChoiceField(
        choices=[('sms', 'SMS'), ('call', 'Call')],
        widget=BootstrapSelect(size=3))

    def clean_country_code(self):
        country_code = self.cleaned_data['country_code']
        if not country_code.startswith('+'):
            country_code = '+' + country_code
        return country_code

    def clean(self):
        data = self.cleaned_data
        phone_number = data['country_code'] + data['phone_number']
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Invalid phone number')
        except NumberParseException as e:
            self.add_error('phone_number', e)


class TokenForm(forms.Form):
    token = forms.CharField(
        widget=BootstrapInput('Verification Token', size=6))
