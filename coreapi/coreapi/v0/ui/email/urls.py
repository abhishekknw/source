from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (SendMail, Mail, EmailSettingsView)
from .tasks import *
urlpatterns = [
    url(r'^send-mail/$', SendMail.as_view()),
    url(r'^mail/$', Mail.as_view()),
    url(r'^send-weekly-leads-mail/$', SendWeeklyLeadsMail.as_view()),
    url(r'^email-settings/$', EmailSettingsView.as_view()),
    url(r'^email-settings/(?P<email_setting_id>[A-Z_a-z0-9]+)/$', EmailSettingsView.as_view()),
    url(r'^send-graph-pdf/$', SendGraphPdf.as_view()),
    url(r'^send-booking-details/(?P<campaign_id>[A-Z_a-z0-9]+)/$', SendBookingDetailMails.as_view()),
    url(r'^send-leads-to-self/$', SendLeadsToSelf.as_view()),
    url(r'^send-pre-hype-mails/(?P<campaign_id>[A-Z_a-z0-9]+)/$', SendPreHypeMails.as_view()),
    url(r'^send-recce-mails/(?P<campaign_id>[A-Z_a-z0-9]+)/$', SendRecceMails.as_view()),
    url(r'^send-pipeline-details/(?P<campaign_id>[A-Z_a-z0-9]+)/$', SendPipelineDetailMails.as_view()),
    url(r'^send-advanced-booking-details/(?P<campaign_id>[A-Z_a-z0-9]+)/$', SendAdvancedBookingDetailMails.as_view()),
    url(r'^send-campaign-assignment/$', SendDailyAssignmentMails.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
