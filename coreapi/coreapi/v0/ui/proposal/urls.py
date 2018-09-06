from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (CreateInitialProposalBulkBasic, HashtagImagesViewSet, InitialProposalAPIView,
                   GetAccountProposalsAPIView, CurrentProposalAPIView, ProposalHistoryAPIView, ChildProposals,
                   CreateInitialProposal, ProposalViewSet, CreateFinalProposal, ProposalVersion, ProposalToCampaign,
                   FinalProposalAPIView, CreateProposalAPIView, ProposalImagesPath, convertDirectProposalToCampaign,
                   CampaignToProposal, SupplierPhaseViewSet)

urlpatterns = [
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

]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^hashtag-images', HashtagImagesViewSet, base_name='hashtag-images')
router.register(r'^supplier-phase', SupplierPhaseViewSet, base_name='supplier-phase')
router.register(r'^proposal', ProposalViewSet, base_name='Proposal')

urlpatterns += router.urls