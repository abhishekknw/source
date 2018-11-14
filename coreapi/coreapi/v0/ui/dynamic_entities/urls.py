from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (CreateEntityType)
urlpatterns = [
    url(r'^create-entity-type/$', CreateEntityType.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
