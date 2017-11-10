from authy.api import AuthyApiClient
from django.conf import settings
from django.shortcuts import render, redirect

from .forms import VerificationForm, TokenForm


authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


def phone_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            request.session['phone_number'] = form.cleaned_data['phone_number']
            request.session['country_code'] = form.cleaned_data['country_code']
            authy_api.phones.verification_start(
                form.cleaned_data['phone_number'],
                form.cleaned_data['country_code'],
                via=form.cleaned_data['via']
            )
            return redirect('token_validation')
    else:
        form = VerificationForm()
    return render(request, 'phone_verification.html', {'form': form})


def token_validation(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = authy_api.phones.verification_check(
                request.session['phone_number'],
                request.session['country_code'],
                form.cleaned_data['token']
            )
            if verification.ok():
                request.session['is_verified'] = True
                return redirect('verified')
            else:
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, 'token_validation.html', {'form': form})


def verified(request):
    if not request.session.get('is_verified'):
        return redirect('phone_verification')
    return render(request, 'verified.html')
