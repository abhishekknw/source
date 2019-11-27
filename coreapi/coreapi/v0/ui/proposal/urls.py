from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (CreateInitialProposalBulkBasic, HashtagImagesViewSet, InitialProposalAPIView,
                   GetAccountProposalsAPIView, CurrentProposalAPIView, ProposalHistoryAPIView, ChildProposals,
                   CreateInitialProposal, ProposalViewSet, CreateFinalProposal, ProposalVersion, ProposalToCampaign,
                   FinalProposalAPIView, CreateProposalAPIView, ProposalImagesPath, convertDirectProposalToCampaign,
                   CampaignToProposal, SupplierPhaseViewSet, getSupplierListByStatus, ImportSheetInExistingCampaign,
                   GetOngoingSuppliersOfCampaign, GetExtraLead, HashtagImagesNewViewSet, SupplierAssignmentViewSet,
                    ConvertProposalToCampaign)

urlpatterns = [
    # url(r'^/create-dummy-proposal/$', CreateDummyProposal.as_view()),
    url(r'^create-initial-proposal-basic/$', CreateInitialProposalBulkBasic.as_view()),
    url(r'^(?P<account_id>[A-Z_a-z0-9]+)/getAccountProposals/$', GetAccountProposalsAPIView.as_view(),
        name='get-account-proposals'),
    url(r'^(?P<account_id>[A-Z_a-z0-9]+)/createInitialProposal/$', InitialProposalAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/currentProposal/$', CurrentProposalAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/getProposalVersion/$', ProposalHistoryAPIView.as_view()),
    url(r'^child-proposals/(?P<proposal_id>[A-Z_a-z0-9-]+)/$', ChildProposals.as_view()),
    url(r'^(?P<account_id>[A-Z_a-z0-9-]+)/create-initial-proposal/$', CreateInitialProposal.as_view(),
        name='create-initial-proposal'),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/create-final-proposal/$', CreateFinalProposal.as_view(),
        name='create-final-proposal'),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/proposal-version/$', ProposalVersion.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/convert-to-campaign/$', ProposalToCampaign.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/createFinalProposal/$', FinalProposalAPIView.as_view(),
        name='create-final-proposal'),
    url(r'^manageCampaign/(?P<id>[A-Z_a-z0-9]+)/proposal/$', CreateProposalAPIView.as_view()),
    url(r'^proposal-images-path/$', ProposalImagesPath.as_view()),
    url(r'^convert-direct-proposal-to-campaign/$', convertDirectProposalToCampaign.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9-]+)/convert-to-proposal/$', CampaignToProposal.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9-]+)/get-suppliers-by-status/$', getSupplierListByStatus.as_view()),
    url(r'^import-sheet-in-existing-campaign/$', ImportSheetInExistingCampaign.as_view()),
    url(r'^get-ongoing-suppliers/(?P<campaign_id>[A-Z_a-z0-9-]+)/$', GetOngoingSuppliersOfCampaign.as_view()),
    url(r'^get-extra-leads/(?P<campaign_id>[A-Z_a-z0-9-]+)/(?P<form_id>[A-Z_a-z0-9-]+)/(?P<supplier_id>[A-Z_a-z0-9-]+)/$', GetExtraLead.as_view()),
    url(r'^hashtag-images-new/$', HashtagImagesNewViewSet.as_view()),
    url(r'^proposal-to-campaign/(?P<proposal_id>[A-Z_a-z0-9-]+)/$', ConvertProposalToCampaign.as_view()),
]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^hashtag-images', HashtagImagesViewSet, base_name='hashtag-images')
router.register(r'^proposal', ProposalViewSet, base_name='Proposal')
router.register(r'^supplier-assignment', SupplierAssignmentViewSet, base_name='supplier-assignment')

urlpatterns += router.urls
