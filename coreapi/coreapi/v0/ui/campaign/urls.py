from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page
from .views import (ShortlistSocietyCountAPIView, BookCampaignAPIView,
                   FinalCampaignBookingAPIView, campaignListAPIVIew, CampaignAPIView, DashBoardViewSet,
                   DeleteInventoryActivityAssignment, GetCampaignAssignments, DeleteCampaignAssignments,
                   GetAdInventoryTypeAndDurationTypeData, AddDynamicInventoryIds, DeleteAdInventoryIds,
                   CampaignLeads, CityWiseMultipleCampaignLeads, PhaseWiseMultipleCampaignLeads, CampaignLeadsCustom,
                   Comment, CampaignLeadsMultiple, GetPermissionBoxImages, CampaignWiseSummary, AssignedCampaigns,
                    VendorWiseSummary, VendorDetails, UserCities, CityWiseSummary, MISReportReceipts, MISReportContacts,
                    AllCampaigns)
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
    url(r'^dashboard/get_leads_by_campaign_new/$',  CampaignLeads.as_view()),
    url(r'^dashboard/proposal_id/get_leads_by_multiple_campaigns/$',  CampaignLeadsMultiple.as_view()),
    url(r'^city-wise-multiple-campaign/$', CityWiseMultipleCampaignLeads.as_view()),
    url(r'^phase-wise-multiple-campaign/$', PhaseWiseMultipleCampaignLeads.as_view()),
    url(r'^dashboard/get_leads_by_campaign_custom/$',  CampaignLeadsCustom.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9-]+)/comment/$', Comment.as_view()),
    # url(r'^update-supplier-phase/$', SupplierPhaseUpdate.as_view()),
    url(r'get-permission-box-images/(?P<campaign_id>[A-Z_a-z0-9]+)/(?P<supplier_id>[A-Z_a-z0-9]+)/$', GetPermissionBoxImages.as_view()),
    #url(r'^fix-invalid-dates/$', FixInvalidDates.as_view()),
    url(r'^campaign-wise-summary/$', CampaignWiseSummary.as_view()),
    url(r'^vendor-wise-summary/$', VendorWiseSummary.as_view()),
    url(r'^city-wise-summary/$', CityWiseSummary.as_view()),
    url(r'^assigned-campaigns/$', AssignedCampaigns.as_view()),
    url(r'^all-campaigns/$', AllCampaigns.as_view()),
    url(r'^vendors-details/$', VendorDetails.as_view()),
    url(r'^user-cities/$', UserCities.as_view()),
    url(r'^mis-report-receipts/$', MISReportReceipts.as_view()),
    url(r'^mis-report-contacts/$', MISReportContacts.as_view())
]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^dashboard', DashBoardViewSet, base_name='dashboard')

urlpatterns += router.urls
