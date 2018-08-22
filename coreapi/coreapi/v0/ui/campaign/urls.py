from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (CampaignInventoryAPIView, ShortlistSocietyCountAPIView, BookCampaignAPIView,
                   FinalCampaignBookingAPIView, CampaignToProposal, campaignListAPIVIew,
                   CampaignsAssignedInventoryCountApiView, GetAssignedIdImagesListApiView)

urlpatterns = [
    url(r'^getCampaigns/$', views.CampaignAPIView.as_view()),
    url(r'campaign/(?P<id>[A-Z_a-z0-9]+)/society/count/$', ShortlistSocietyCountAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/book/$', BookCampaignAPIView.as_view()),
    url(r'^finalbooking/(?P<id>[A-Z_a-z0-9]+)/$', FinalCampaignBookingAPIView.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9-]+)/convert-to-proposal/$', CampaignToProposal.as_view()),
    url(r'^campaign-list/(?P<organisation_id>[A-Z_a-z0-9-]+)/$', campaignListAPIVIew.as_view()),
    url(r'^campaigns-assigned-inventory-counts/(?P<organisation_id>[A-Z_a-z0-9-]+)/$',CampaignsAssignedInventoryCountApiView.as_view()),
    url(r'^campaigns-assigned-inventory-ids-and-images/(?P<organisation_id>[A-Z_a-z0-9-]+)/$', GetAssignedIdImagesListApiView.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^dashboard', views.DashBoardViewSet, base_name='dashboard')

urlpatterns += router.urls
