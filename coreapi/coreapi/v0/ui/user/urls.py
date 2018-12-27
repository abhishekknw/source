from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (UserAPI, UserAPISelf)

urlpatterns = [
    url(r'^self', UserAPISelf.as_view()),
    url(r'^', UserAPI.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
