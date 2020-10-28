from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (ImportLead, RequirementClass, SuspenseLeadClass, BrowsedLeadClass, LeadOpsVerification, BrowsedToRequirement, DeleteRequirement, BrowsedLeadDelete, RestoreRequirement, BdVerification)

urlpatterns = [
    url(r'^import-lead/(?P<campaign_id>[A-Z_a-z0-9]+)/$', ImportLead.as_view()),
    url(r'^requirements/$', RequirementClass.as_view()),
    url(r'^suspance-leads/$', SuspenseLeadClass.as_view()),
    url(r'^browsed-leads/$', BrowsedLeadClass.as_view()),
    url(r'^ops-lead-verification/$', LeadOpsVerification.as_view()),
    url(r'^browsed-to-requirement/$', BrowsedToRequirement.as_view()),
    url(r'^delete-requirement/$', DeleteRequirement.as_view()),
    url(r'^delete-browsed-lead/$', BrowsedLeadDelete.as_view()),
    url(r'^restore-requirement/$', RestoreRequirement.as_view()),
    url(r'^bd-verification/$', BdVerification.as_view()),
]

# router = DefaultRouter()
# router.include_format_suffixes = False
# urlpatterns += router.urls