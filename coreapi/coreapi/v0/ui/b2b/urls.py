from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (ImportLead, RequirementClass, SuspenseLeadClass, BrowsedLeadClass)

urlpatterns = [
    url(r'^import-lead/(?P<campaign_id>[A-Z_a-z0-9]+)/$', ImportLead.as_view()),
    url(r'^requirements/$', RequirementClass.as_view()),
    url(r'^requirements/$', RequirementClass.as_view()),
    url(r'^suspance-leads/$', SuspenseLeadClass.as_view()),
    url(r'^browsed-leads/$', BrowsedLeadClass.as_view())
]

# router = DefaultRouter()
# router.include_format_suffixes = False
# urlpatterns += router.urls