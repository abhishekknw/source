from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^audit/', include('v0.android.audit.urls')),

                       )
