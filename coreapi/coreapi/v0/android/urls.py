from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^audit/', include('v0.android.audit.urls'))
    ]
