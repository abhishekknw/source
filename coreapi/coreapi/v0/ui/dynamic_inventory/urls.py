from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (BaseInventoryAPI, BaseInventoryAPIById, InventoryAPI, InventoryAPIById)

urlpatterns = [
    url(r'^base-inventory/$', BaseInventoryAPI.as_view()),
    url(r'^base-inventory/(?P<base_inventory_id>[A-Z_a-z0-9]+)/$', BaseInventoryAPIById.as_view()),
    url(r'^inventory/$', InventoryAPI.as_view()),
    url(r'^inventory/(?P<inventory_id>[A-Z_a-z0-9]+)/$', InventoryAPIById.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
