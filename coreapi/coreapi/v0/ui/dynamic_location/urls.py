from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    url(r'^state/$', State.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls