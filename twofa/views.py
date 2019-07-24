from authy.api import AuthyApiClient
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


from .decorators import twofa_required
from .forms import RegistrationForm, TokenVerificationForm
from .models import TwoFAUser


authy_api = AuthyApiClient(settings.ACCOUNT_SECURITY_API_KEY)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            authy_user = authy_api.users.create(
                form.cleaned_data['email'],
                form.cleaned_data['phone_number'],
                form.cleaned_data['country_code'],
            )
            if authy_user.ok():
                twofa_user = TwoFAUser.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    authy_user.id,
                    form.cleaned_data['password']
                )
                login(request, twofa_user)
                return redirect('2fa')
            else:
                for key, value in authy_user.errors().items():
                    form.add_error(
                        None,
                        '{key}: {value}'.format(key=key, value=value)
                    )
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def twofa(request):
    if request.method == 'POST':
        form = TokenVerificationForm(request.POST)
        if form.is_valid(request.user.authy_id):
            request.session['authy'] = True
            return redirect('protected')
    else:
        form = TokenVerificationForm()
    return render(request, '2fa.html', {'form': form})


@login_required
def token_sms(request):
    sms = authy_api.users.request_sms(request.user.authy_id, {'force': True})
    if sms.ok():
        return HttpResponse('SMS request successful', status=200)
    else:
        return HttpResponse('SMS request failed', status=503)


@login_required
def token_voice(request):
    call = authy_api.users.request_call(request.user.authy_id, {'force': True})
    if call.ok():
        return HttpResponse('Call request successfull', status=200)
    else:
        return HttpResponse('Call request failed', status=503)


@login_required
def token_onetouch(request):
    details = {
        'Authy ID': request.user.authy_id,
        'Username': request.user.username,
        'Reason': 'Demo by Account Security'
    }

    hidden_details = {
        'test': 'This is a'
    }

    response = authy_api.one_touch.send_request(
        int(request.user.authy_id),
        message='Login requested for Account Security account.',
        seconds_to_expire=120,
        details=details,
        hidden_details=hidden_details
    )
    if response.ok():
        request.session['onetouch_uuid'] = response.get_uuid()
        return HttpResponse('OneTouch request successfull', status=200)
    else:
        return HttpResponse('OneTouch request failed', status=503)


@login_required
def onetouch_status(request):
    uuid = request.session['onetouch_uuid']
    approval_status = authy_api.one_touch.get_approval_status(uuid)
    if approval_status.ok():
        if approval_status['approval_request']['status'] == 'approved':
            request.session['authy'] = True
        return HttpResponse(
            approval_status['approval_request']['status'],
            status=200
        )
    else:
        return HttpResponse(approval_status.errros(), status=503)


@twofa_required
def protected(request):
    return render(request, 'protected.html')
