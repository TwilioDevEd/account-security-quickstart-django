import functools
from django.conf import settings
from django.shortcuts import redirect


def twofa_required(view):
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if request.session.get('authy', False):
            return view(request, *args, **kwargs)
        return redirect('2fa')
    return wrapper
