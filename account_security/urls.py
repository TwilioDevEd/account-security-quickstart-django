from django.conf.urls import url
from django.contrib.auth import views as auth_views

from twofa import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^2fa/$', views.twofa, name='2fa'),
    url(r'^token/sms$', views.token_sms, name='token-sms'),
    url(r'^token/voice$', views.token_voice, name='token-voice'),
    url(r'^token/onetouch$', views.token_onetouch, name='token-onetouch'),
    url(r'^protected/$', views.protected, name='protected'),
    url(r'^onetouch-status$', views.onetouch_status, name='onetouch-status'),
]
