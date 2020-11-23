from __future__ import absolute_import
from django.conf.urls import url
from .views import UpdateSupplierContactDataImport, CreateSupplierWithContactDetails, DeleteDuplicateSocieties, AddBookingStatus, AddBookingSubstatus, storeS3UrlToCSV, DeleteUser, UpdateLandmark

urlpatterns = [
    url(r'^import-supplier-contact-data-from-sheet/$', UpdateSupplierContactDataImport.as_view()),
    url(r'^import-suppliers-from-sheet/$', CreateSupplierWithContactDetails.as_view()),
    url(r'^delete-duplicate-societies/$', DeleteDuplicateSocieties.as_view()),
    url(r'^add-booking-status/$', AddBookingStatus.as_view()),
    url(r'^add-booking-substatus/$', AddBookingSubstatus.as_view()),
    url(r'^update-supplier-contact/$', UpdateSupplierContactDataImport.as_view()),
    url(r'^create-multiple-suppliers/$', CreateSupplierWithContactDetails.as_view()),
    url(r'^store-product_ids/$', storeS3UrlToCSV.as_view()),
    url(r'^delete-user/$', DeleteUser.as_view()),
    url(r'^update-landmark/$', UpdateLandmark.as_view()),
]