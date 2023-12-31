from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (AlternateApiGetDataFromBot,MobileNumberVerification, GetDataFromBot, GetDataFromBotToSheet)

urlpatterns = [
    url(r'^mobile-verification/$', MobileNumberVerification.as_view()),
    url(r'^bot-data/$', GetDataFromBot.as_view()),
    url(r'^bot-to-sheet/$', GetDataFromBotToSheet.as_view()),
    url(r'^bot-data-2/$', AlternateApiGetDataFromBot.as_view()),
]

# router = DefaultRouter()
# router.include_format_suffixes = False
# urlpatterns += router.urls