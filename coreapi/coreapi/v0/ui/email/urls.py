from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (SendMail, Mail, EmailSettingsView)
from tasks import SendWeeklyLeadsMail, SendGraphPdf, SendBookingDetailMails, SendLeadsToSelf, SendPipelineDetailMails
urlpatterns = [
    url(r'^send-mail/$', SendMail.as_view()),
    url(r'^mail/$', Mail.as_view()),
    url(r'^send-weekly-leads-mail/$', SendWeeklyLeadsMail.as_view()),
    url(r'^email-settings/$', EmailSettingsView.as_view()),
    url(r'^email-settings/(?P<email_setting_id>[A-Z_a-z0-9]+)/$', EmailSettingsView.as_view()),
    url(r'^send-graph-pdf/$', SendGraphPdf.as_view()),
    url(r'^send-booking-details/$', SendBookingDetailMails.as_view()),
    url(r'^send-leads-to-self/$', SendLeadsToSelf.as_view()),
    url(r'^send-pipeline-details/$', SendPipelineDetailMails.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
