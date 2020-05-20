from __future__ import absolute_import
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from .views import (TransactionDataImport, SocietyDataImport, FilteredSuppliersAPIView, ImportSocietyData,
                    ImportContactDetails, FilteredSuppliers, SupplierSearch, SupplierDetails,
                    ImportSupplierDataFromSheet, ImportSupplierData, addSupplierDirectToCampaign, deleteSuppliers,
                    deleteShortlistedSpaces, insertFlatCountType, listCampaignSuppliers, CreateSupplierPriceMappingObjects,
                    GetLocationDataInSheet, MultiSupplierDetails, SupplierRetailShop)

urlpatterns = [
    url(r'^society-transaction-data-import-excel/$', TransactionDataImport.as_view()),
    url(r'^society-data-import-excel/$', SocietyDataImport.as_view()),
    url(r'^getFilteredSocieties/$', FilteredSuppliersAPIView.as_view()),
    url(r'^save-society-data/$', ImportSocietyData.as_view()),
    url(r'^save-contact-details/$', ImportContactDetails.as_view()),
    url(r'^filtered-suppliers/$', FilteredSuppliers.as_view()),
    url(r'^supplier-search/$', SupplierSearch.as_view()),
    url(r'^supplier-details/$', SupplierDetails.as_view()),
    url(r'^import-supplier-data-from-sheet/$', ImportSupplierDataFromSheet.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/import-supplier-data/$', ImportSupplierData.as_view()),
    url(r'^add-suppliers-direct-to-campaign/$', addSupplierDirectToCampaign.as_view()),
    url(r'^delete-suppliers/$', deleteSuppliers.as_view()),
    url(r'^delete-shortlisted-spaces/$', deleteShortlistedSpaces.as_view()),
    url(r'^refresh-flat-count-type/$', insertFlatCountType.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/list_suppliers/$', listCampaignSuppliers.as_view()),
    url(r'^create_pmd_for_supplier/$', CreateSupplierPriceMappingObjects.as_view()),
    url(r'^get-location-data-in-sheet/$', GetLocationDataInSheet.as_view()),
    url(r'^multi-supplier-details/$', MultiSupplierDetails.as_view()),
    url(r'^supplier-retail-mapping/$', SupplierRetailShop.as_view()),
]

