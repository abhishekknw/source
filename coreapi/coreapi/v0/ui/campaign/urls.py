from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (ShortlistSocietyCountAPIView, BookCampaignAPIView,
                   FinalCampaignBookingAPIView, campaignListAPIVIew, CampaignAPIView, DashBoardViewSet,
                   DeleteInventoryActivityAssignment, GetCampaignAssignments, DeleteCampaignAssignments,
                   GetAdInventoryTypeAndDurationTypeData, AddDynamicInventoryIds, DeleteAdInventoryIds)
from v0.ui.website.views import (GetAssignedIdImagesListApiView)

urlpatterns = [
    url(r'^getCampaigns/$', CampaignAPIView.as_view()),
    url(r'campaign/(?P<id>[A-Z_a-z0-9]+)/society/count/$', ShortlistSocietyCountAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/book/$', BookCampaignAPIView.as_view()),
    url(r'^finalbooking/(?P<id>[A-Z_a-z0-9]+)/$', FinalCampaignBookingAPIView.as_view()),
    url(r'^campaign-list/(?P<organisation_id>[A-Z_a-z0-9-]+)/$', campaignListAPIVIew.as_view()),
    url(r'^campaigns-assigned-inventory-ids-and-images/(?P<organisation_id>[A-Z_a-z0-9-]+)/$', GetAssignedIdImagesListApiView.as_view()),
    url(r'^delete-inv-activity-assignment/(?P<id>[A-Z_a-z0-9]+)/$', DeleteInventoryActivityAssignment.as_view()),
    url(r'^view-campaign-assignments/(?P<campaign_id>[A-Z_a-z0-9]+)/$', GetCampaignAssignments.as_view()),
    url(r'^delete-campaign-assignments/(?P<assignment_id>[A-Z_a-z0-9]+)/$', DeleteCampaignAssignments.as_view()),
    url(r'^get-adinventorytype-and-durationtype-data/$', GetAdInventoryTypeAndDurationTypeData.as_view()),
    url(r'^add-dynamic-inventory-ids/$', AddDynamicInventoryIds.as_view()),
    url(r'^delete-ad-inventory-ids/$', DeleteAdInventoryIds.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^dashboard', DashBoardViewSet, base_name='dashboard')

urlpatterns += router.urls
