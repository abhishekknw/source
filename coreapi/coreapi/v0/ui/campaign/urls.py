from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (ShortlistSocietyCountAPIView, BookCampaignAPIView,
                   FinalCampaignBookingAPIView, campaignListAPIVIew, CampaignAPIView, DashBoardViewSet)
from v0.ui.website.views import (GetAssignedIdImagesListApiView)

urlpatterns = [
    url(r'^getCampaigns/$', CampaignAPIView.as_view()),
    url(r'campaign/(?P<id>[A-Z_a-z0-9]+)/society/count/$', ShortlistSocietyCountAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/book/$', BookCampaignAPIView.as_view()),
    url(r'^finalbooking/(?P<id>[A-Z_a-z0-9]+)/$', FinalCampaignBookingAPIView.as_view()),
    url(r'^campaign-list/(?P<organisation_id>[A-Z_a-z0-9-]+)/$', campaignListAPIVIew.as_view()),
    url(r'^campaigns-assigned-inventory-ids-and-images/(?P<organisation_id>[A-Z_a-z0-9-]+)/$', GetAssignedIdImagesListApiView.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^dashboard', DashBoardViewSet, base_name='dashboard')

urlpatterns += router.urls