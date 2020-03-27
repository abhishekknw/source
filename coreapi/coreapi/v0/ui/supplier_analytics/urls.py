from __future__ import absolute_import
from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^supplier-count/(?P<supplier_type>[A-Z]{2})/$', GetSupplierCitywiseCount.as_view()),
    url(r'^supplier-list/(?P<supplier_type>[A-Z]{2})/$', GetSupplierList.as_view()),
]
