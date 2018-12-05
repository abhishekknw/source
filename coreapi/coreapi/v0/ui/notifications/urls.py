from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (NotificationsAPI, NotificationsMarkReadAPI)

urlpatterns = [
    url(r'^(?P<notification_id>[A-Z_a-z0-9]+)/mark_read/$', NotificationsMarkReadAPI.as_view()),
    url(r'^', NotificationsAPI.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
