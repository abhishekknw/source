from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (NotificationsAPI)

urlpatterns = [
    url(r'^', NotificationsAPI.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
