from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (SendMail, Mail, SendWeeklyLeadsMail, EmailSettingsView)

urlpatterns = [
    url(r'^send-mail/$', SendMail.as_view()),
    url(r'^mail/$', Mail.as_view()),
    url(r'^send-weekly-leads-mail/$', SendWeeklyLeadsMail.as_view()),
    url(r'^email-settings/$', EmailSettingsView.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
