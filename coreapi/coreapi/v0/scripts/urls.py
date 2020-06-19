from __future__ import absolute_import
from django.conf.urls import url
from .views import UpdateSupplierContactDataImport, CreateSupplierWithContactDetails, DeleteDuplicateSocieties,storeS3UrlToCSV, DeleteUser

urlpatterns = [
    url(r'^update-supplier-contact/$', UpdateSupplierContactDataImport.as_view()),
    url(r'^create-multiple-suppliers/$', CreateSupplierWithContactDetails.as_view()),
    url(r'^delete-duplicate-societies/$', DeleteDuplicateSocieties.as_view()),
    url(r'^store-product_ids/$', storeS3UrlToCSV.as_view()),
    url(r'^delete-user/$', DeleteUser.as_view())
]