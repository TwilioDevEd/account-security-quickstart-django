from django.shortcuts import render, redirect

from lib import twilio_client
from .forms import VerificationForm, TokenForm


def phone_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            request.session['phone_number'] = form.cleaned_data['phone_number']
            verification = twilio_client.verifications(form.cleaned_data['phone_number'], form.cleaned_data['via'])
            return redirect('token_validation')
    else:
        form = VerificationForm()
    return render(request, 'phone_verification.html', {'form': form})


def token_validation(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = twilio_client.verification_checks(request.session['phone_number'], form.cleaned_data['token'])

            if verification.status == 'approved':
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
