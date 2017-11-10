from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from twofa import views as twofa_views
from phone_verification import views as verify_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^register/$', twofa_views.register, name='register'),
    url(r'^2fa/$', twofa_views.twofa, name='2fa'),
    url(r'^token/sms$', twofa_views.token_sms, name='token-sms'),
    url(r'^token/voice$', twofa_views.token_voice, name='token-voice'),
    url(r'^token/onetouch$', twofa_views.token_onetouch, name='token-onetouch'),  # noqa: E501
    url(r'^protected/$', twofa_views.protected, name='protected'),
    url(r'^onetouch-status$', twofa_views.onetouch_status, name='onetouch-status'),  # noqa: E501

    url(r'^verification/$', verify_views.phone_verification, name='phone_verification'),  # noqa: E501
    url(r'^verification/token/$', verify_views.token_validation, name='token_validation'),  # noqa: E501
    url(r'^verified/$', verify_views.verified, name='verified'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
