from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from v0.ui.website import views
from v0.ui.campaign.views import CreateSupplierPhaseData
from v0.ui.proposal.views import SupplierPhaseViewSet
urlpatterns = [

    url(r'^campaign/society/shortlist/$', views.ShortlistSocietyAPIView.as_view()),

    # Beta Urls and Classes
    url(r'^(?P<proposal_id>[A-Z_a-z0-9]+)/getSpaces/$', views.SpacesOnCenterAPIView.as_view(), name='get-spaces'),
    # url(r'^getSpace/(?P<id>[A-Z_a-z0-9]+)/$', views.GetSpaceInfoAPIView.as_view()),

    # for saving societies
    #url(r'^putSocietiesInTable/$', views.SocietySaveCSVAPIView.as_view()),
    url(r'^save-corporate-data/$', views.ImportCorporateData.as_view()),

    url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/export-spaces-data/$', views.GenericExportData.as_view()),
    # url(r'^import-campaign-leads-data/$', views.ImportCampaignLeads.as_view()),
    url(r'^import-area-subarea/$', views.ImportAreaSubArea.as_view()),
    url(r'^send-mail/$', views.SendMail.as_view()),
    url(r'^business-data/$', views.Business.as_view()),
    url(r'^mail/$', views.Mail.as_view()),
    url(r'^campaign-assignment/$', views.AssignCampaign.as_view()),
    url(r'^amenity/$', views.AmenityAPIView.as_view()),
    url(r'^amenity-list/$', views.GetAllAmenities.as_view()),
    url(r'^supplier-amenity/$', views.SupplierAmenity.as_view()),
    url(r'^get-users-list/$', views.UserList.as_view()),
    url(r'^bulk-download-images-amazon/$', views.BulkDownloadImagesAmazon.as_view()),
    url(r'^task/is-group-task-successfull/(?P<task_id>.+)/$', views.IsGroupTaskSuccessFull.as_view()),
    url(r'^task/is-individual-task-successfull/(?P<task_id>.+)/$', views.IsIndividualTaskSuccessFull.as_view()),
    url(r'^delete-file-from-system/$', views.DeleteFileFromSystem.as_view()),
    url(r'^export-all-supplier_data/$', views.ExportAllSupplierData.as_view()),
    url(r'^clone-profile/$', views.CloneProfile.as_view()),
    url(r'^get-relationship-and-past-campaigns-data/$', views.GetRelationshipAndPastCampaignsData.as_view()),
    url(r'^create-supplier-phase-data/$', CreateSupplierPhaseData.as_view())
]

router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'^contact', views.ContactViewSet, base_name='Contact')
router.register(r'^profile', views.ProfileViewSet, base_name='Profile')
router.register(r'^content-type', views.ContentTypeViewSet, base_name='Content-Type')
router.register(r'^organisation', views.OrganisationViewSet, base_name='Organisation')
router.register(r'^organisation-map', views.OrganisationMapViewSet, base_name='organisation-map')
router.register(r'^proposal-center-mapping', views.proposalCenterMappingViewSet, base_name='proposal-center-mapping')
router.register(r'^supplier-phase', SupplierPhaseViewSet, base_name='supplier-phase')

urlpatterns += router.urls
