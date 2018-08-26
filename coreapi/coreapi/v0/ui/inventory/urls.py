from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (CampaignInventory, CampaignSuppliersInventoryList, InventoryActivityImageAPIView,
                   BulkInsertInventoryActivityImage, GenerateInventoryActivitySummary,
                   InventoryActivityAssignmentAPIView, AssignInventoryActivityDateUsers,
                   ReassignInventoryActivityDateUsers, CampaignsAssignedInventoryCountApiView,
                   CampaignInventoryAPIView, UploadInventoryActivityImageAmazon)

urlpatterns = [
    url(r'^(?P<campaign_id>[A-Z_a-z0-9-]+)/campaign-inventories/$', CampaignInventory.as_view()),
    url(r'^campaigns-suppliers-inventory-list/$', CampaignSuppliersInventoryList.as_view()),
    url(r'^inventory-activity-image/$', InventoryActivityImageAPIView.as_view()),
    url(r'^bulk-update-inventory-activity-image/$', BulkInsertInventoryActivityImage.as_view()),
    url(r'^generate-inventory-activity-summary/$', GenerateInventoryActivitySummary.as_view()),
    url(r'^inventory-activity-assignment/$', InventoryActivityAssignmentAPIView.as_view()),
    url(r'^inventory-activity-date-user-assignment/$', AssignInventoryActivityDateUsers.as_view()),
    url(r'^inventory-activity-date-user-reassignment/$', ReassignInventoryActivityDateUsers.as_view()),
    url(r'^upload-inventory-activity-image-amazon/$', UploadInventoryActivityImageAmazon.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/inventories/$', CampaignInventoryAPIView.as_view()),
    url(r'^campaigns-assigned-inventory-counts/(?P<organisation_id>[A-Z_a-z0-9-]+)/$',CampaignsAssignedInventoryCountApiView.as_view()),

]

router = DefaultRouter()
router.include_format_suffixes = False

urlpatterns += router.urls
