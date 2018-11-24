from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (EntityType, EntityTypeById, Entity, EntityById)

urlpatterns = [
    url(r'^entity-type/$', EntityType.as_view()),
    url(r'^entity-type/(?P<entity_type_id>[A-Z_a-z0-9]+)/$', EntityTypeById.as_view()),
    url(r'^entity/$', Entity.as_view()),
    url(r'^entity/(?P<entity_id>[A-Z_a-z0-9]+)/$', EntityById.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
