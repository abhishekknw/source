from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (SupplierType, SupplierTypeById, Supplier, SupplierById,SupplierTransfer, ShortlistedSpacesTransfer)
from .base_supplier_type import BaseSupplierType, BaseSupplierTypeById

urlpatterns = [
    url(r'^supplier-type/$', SupplierType.as_view()),
    url(r'^supplier-type/(?P<supplier_type_id>[A-Z_a-z0-9]+)/$', SupplierTypeById.as_view()),
    url(r'^supplier/$', Supplier.as_view()),
    url(r'^supplier/(?P<supplier_id>[A-Z_a-z0-9]+)/$', SupplierById.as_view()),
    url(r'^base-supplier-type/$', BaseSupplierType.as_view()),
    url(r'^base-supplier-type/(?P<base_supplier_type_id>[A-Z_a-z0-9]+)/$', BaseSupplierTypeById.as_view()),
    url(r'^societies-add/$', SupplierTransfer.as_view()),
    url(r'^shortlisted-spaces-add/$', ShortlistedSpacesTransfer.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
