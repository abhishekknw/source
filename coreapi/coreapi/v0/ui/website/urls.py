from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from v0.ui.website import views

urlpatterns = [

    url(r'^businesses/$', views.BusinessAPIListView.as_view(), name='get-all-business-info'),
    url(r'^business/(?P<id>[A-Z_a-z0-9]+)$', views.BusinessAccounts.as_view(), name='get-one-business-data'),
    url(r'^accounts/$', views.Accounts.as_view()),
    url(r'^account/(?P<id>[A-Z_a-z0-9]+)$', views.AccountAPIView.as_view()),
    url(r'^newCampaign/$', views.BusinessContacts.as_view()),
    url(r'^newAccountCampaign/$', views.AccountContacts.as_view()),

    url(r'^(?P<account_id>[A-Z_a-z0-9]+)/getAccountProposals/$', views.GetAccountProposalsAPIView.as_view(), name='get-account-proposals'),

    url(r'^getCampaigns/$', views.CampaignAPIView.as_view()),
    url(r'^manageCampaign/(?P<id>[A-Z_a-z0-9]+)/proposal/$', views.CreateProposalAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/inventories/$', views.CampaignInventoryAPIView.as_view()),

    url(r'campaign/(?P<id>[A-Z_a-z0-9]+)/society/count/$',views.ShortlistSocietyCountAPIView.as_view()),

    url(r'^campaign/society/shortlist/$', views.ShortlistSocietyAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/book/$', views.BookCampaignAPIView.as_view()),
    url(r'^finalbooking/(?P<id>[A-Z_a-z0-9]+)/$', views.FinalCampaignBookingAPIView.as_view()),
    url(r'^create_business/load_business_types/$', views.GetBusinessTypesAPIView.as_view(), name='get-business-types'),
    url(r'^subtypes/(?P<id>[A-Z_a-z0-9]+)/$', views.GetBusinessSubTypesAPIView.as_view(), name='get-business-subtypes'),

    # Beta Urls and Classes
    url(r'^(?P<account_id>[A-Z_a-z0-9]+)/createInitialProposal/$',views.InitialProposalAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/createFinalProposal/$',views.FinalProposalAPIView.as_view(), name='create-final-proposal'),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/getSpaces/$', views.SpacesOnCenterAPIView.as_view(), name='get-spaces'),
    # url(r'^getSpace/(?P<id>[A-Z_a-z0-9]+)/$', views.GetSpaceInfoAPIView.as_view()),
    url(r'^getFilteredSocieties/$', views.FilteredSuppliersAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/currentProposal/$',views.CurrentProposalAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/getProposalVersion/$', views.ProposalHistoryAPIView.as_view()),

    # for saving societies
    #url(r'^putSocietiesInTable/$', views.SocietySaveCSVAPIView.as_view()),
    url(r'^save-society-data/$', views.ImportSocietyData.as_view()),
    url(r'^save-contact-details/$', views.ImportContactDetails.as_view()),
    url(r'^save-corporate-data/$', views.ImportCorporateData.as_view()),

    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/export-spaces-data/$', views.GenericExportData.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/import-supplier-data/$', views.ImportSupplierData.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/import-proposal-cost-data/$', views.ImportProposalCostData.as_view(), name='import-metric-data'),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/create-final-proposal/$', views.CreateFinalProposal.as_view(), name='create-final-proposal'),
    url(r'^(?P<account_id>[A-Z_a-z0-9-]+)/create-initial-proposal/$', views.CreateInitialProposal.as_view(), name='create-initial-proposal'),
    url(r'^import-campaign-leads-data/$', views.ImportCampaignLeads.as_view()),
    url(r'^filtered-suppliers/$', views.FilteredSuppliers.as_view()),
    url(r'^supplier-search/$', views.SupplierSearch.as_view()),
    url(r'^import-area-subarea/$', views.ImportAreaSubArea.as_view()),
    url(r'^send-mail/$', views.SendMail.as_view()),
    url(r'^business-data/$', views.Business.as_view()),
    url(r'^mail/$', views.Mail.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/proposal-version/$', views.ProposalVersion.as_view()),
    url(r'^campaign-assignment/$', views.AssignCampaign.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9-]+)/campaign-inventories/$', views.CampaignInventory.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/convert-to-campaign/$', views.ProposalToCampaign.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9-]+)/convert-to-proposal/$', views.CampaignToProposal.as_view()),
    url(r'^campaigns-inventory-list/$', views.CampaignInventoryList.as_view()),
    url(r'^inventory-activity-image/$', views.InventoryActivityImage.as_view()),
    url(r'^supplier-details/$', views.SupplierDetails.as_view()),

]

router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'^proposal', views.ProposalViewSet, base_name='Proposal')
urlpatterns += router.urls
