from __future__ import absolute_import
from django.conf.urls import url
from .views import UpdateSupplierContactDataImport, CreateSupplierWithContactDetails, DeleteDuplicateSocieties,storeS3UrlToCSV

urlpatterns = [
    url(r'^import-supplier-contact-data-from-sheet/$', UpdateSupplierContactDataImport.as_view()),
    url(r'^create-multiple-suppliers/$', CreateSupplierWithContactDetails.as_view()),
    url(r'^delete-duplicate-societies/$', DeleteDuplicateSocieties.as_view()),
    url(r'^store-product_ids/$', storeS3UrlToCSV.as_view())
]