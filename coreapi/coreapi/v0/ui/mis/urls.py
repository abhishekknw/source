from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import GetMISData

urlpatterns = [
    url(r'^get-mis-data/', GetMISData.as_view()),
]