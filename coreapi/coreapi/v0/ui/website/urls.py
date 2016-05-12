from django.conf.urls import include, url
from v0.ui.website import views

urlpatterns = [

    url(r'^businesses/$', views.BusinessAPIListView.as_view()),
    url(r'^business/(?P<id>[A-Z_a-z0-9]+)$', views.BusinessAPIView.as_view()),
    url(r'^newCampaign/$', views.NewCampaignAPIView.as_view()),
    url(r'^getCampaigns/$', views.CampaignAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/inventories/$', views.CampaignInventoryAPIView.as_view()),
    url(r'^campaign/society/shortlist/$', views.ShortlistSocietyAPIView.as_view()),
    url(r'^campaign/(?P<id>[A-Z_a-z0-9]+)/book/$', views.BookCampaignAPIView.as_view()),
    url(r'^finalbooking/(?P<id>[A-Z_a-z0-9]+)/$', views.FinalCampaignBookingAPIView.as_view()),

]
