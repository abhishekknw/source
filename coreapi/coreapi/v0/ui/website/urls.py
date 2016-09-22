from django.conf.urls import include, url
from v0.ui.website import views

urlpatterns = [

    url(r'^businesses/$', views.BusinessAPIListView.as_view()),
    url(r'^business/(?P<id>[A-Z_a-z0-9]+)$', views.BusinessAPIView.as_view()),
    url(r'^accounts/$', views.AccountAPIListView.as_view()),
    url(r'^account/(?P<id>[A-Z_a-z0-9]+)$', views.AccountAPIView.as_view()),
    url(r'^newCampaign/$', views.NewCampaignAPIView.as_view()),
    url(r'^newAccountCampaign/$', views.CreateCampaignAPIView.as_view()),

    url(r'^(?P<account_id>[A-Z_a-z0-9]+)/getAccountProposals/$', views.GetAccountProposalsAPIView.as_view()),

    url(r'^getCampaigns/$', views.CampaignAPIView.as_view()),
    url(r'^manageCampaign/(?P<id>[A-Z_a-z0-9]+)/proposal/$', views.CreateProposalAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/inventories/$', views.CampaignInventoryAPIView.as_view()),

    url(r'campaign/(?P<id>[A-Z_a-z0-9]+)/society/count/$',views.ShortlistSocietyCountAPIView.as_view()),

    url(r'^campaign/society/shortlist/$', views.ShortlistSocietyAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/book/$', views.BookCampaignAPIView.as_view()),
    url(r'^finalbooking/(?P<id>[A-Z_a-z0-9]+)/$', views.FinalCampaignBookingAPIView.as_view()),
    url(r'^create_business/load_business_types/$', views.getBusinessTypesAPIView.as_view()),
    url(r'^subtypes/(?P<id>[A-Z_a-z0-9]+)/$', views.getBusinessSubTypesAPIView.as_view()),

    # Beta Urls and Classes
    url(r'^(?P<account_id>[A-Z_a-z0-9]+)/createInitialProposal/$',views.InitialProposalAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/createFinalProposal/$',views.FinalProposalAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/getSpaces/$', views.SpacesOnCenterAPIView.as_view()),
    # url(r'^getSpace/(?P<id>[A-Z_a-z0-9]+)/$', views.GetSpaceInfoAPIView.as_view()),
    url(r'^getFilteredSocieties/$', views.GetFilteredSocietiesAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/currentProposal/$',views.CurrentProposalAPIView.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/getProposalVersion/$', views.ProposalHistoryAPIView.as_view()),

    # for saving societies
    #url(r'^putSocietiesInTable/$', views.SocietySaveCSVAPIView.as_view()),
    url(r'^save-society-data/$', views.SaveSocietyData.as_view()),
    url(r'^save-contact-details/$', views.SaveContactDetails.as_view()),
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/export-spaces-data/$', views.ExportData.as_view()),
]
