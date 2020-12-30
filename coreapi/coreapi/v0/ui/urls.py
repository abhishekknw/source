from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from v0.ui import views

from v0.ui.supplier.views import SocietyListByNumber, SocietyAPIView, SocietyAPIFiltersView, SocietyAPIFiltersListView, SocietyList, \
    SocietyAPISortedListView, SocietyAPISocietyIdsView, GenerateSupplierIdAPIView, checkSupplierCodeAPIView, \
    SupplierImageDetails, CorporateViewSet, GymViewSet, SalonViewSet, RetailShopViewSet, EducationalInstituteViewSet, HordingViewSet, BusShelter, \
    BusShelterSearchView, getBusShelter, SaveBasicCorporateDetailsAPIView, SaveBuildingDetailsAPIView, CompanyDetailsAPIView, \
    CorporateCompanyDetailsAPIView, saveBasicSalonDetailsAPIView, saveBasicGymDetailsAPIView, BusShelter, \
    SuppliersMeta, SuppliersMetaData, BusDepotViewSet, SocietyDataImport, SupplierGenericViewSet
from v0.ui.supplier.supplier_uploads import CorporateParkDataImport

# from v0.ui.website import views as web_views
urlpatterns = [

    url(r'^leads/', include('v0.ui.leads.urls')),
    url(r'^resident/', include('v0.ui.society_resident_details.urls')),
    url(r'^checklists/', include('v0.ui.checklists.urls')),
    url(r'^dynamic-suppliers/', include('v0.ui.dynamic_suppliers.urls')),
    url(r'^dynamic-inventory/', include('v0.ui.dynamic_inventory.urls')),
    url(r'^dynamic-booking/', include('v0.ui.dynamic_booking.urls')),
    url(r'^dynamic-location/', include('v0.ui.dynamic_location.urls')),
    url(r'^notifications/', include('v0.ui.notifications.urls')),
    url(r'^ops/', include('v0.ui.campaign_analytics.urls')),
    url(r'^ops/', include('v0.ui.supplier_analytics.urls')),
    url(r'^users/', include('v0.ui.user.urls')),
    url(r'^accounts/', include('v0.ui.account.urls')),
    url(r'^website/', include('v0.ui.account.urls')),
    url(r'^website/', include('v0.ui.campaign.urls')),
    url(r'^campaign/', include('v0.ui.campaign.urls')),
    url(r'^website/', include('v0.ui.finances.urls')),
    url(r'^website/', include('v0.ui.inventory.urls')),
    url(r'^website/', include('v0.ui.permissions.urls')),
    url(r'^website/', include('v0.ui.proposal.urls')),
    url(r'^proposal/', include('v0.ui.proposal.urls')),
    url(r'^website/', include('v0.ui.supplier.urls')),
    url(r'^website/', include('v0.ui.email.urls')),
    url(r'^website/', include('v0.ui.website.urls')),
    url(r'^analytics/', include('v0.ui.analytics.urls')),
    url(r'^mis/', include('v0.ui.mis.urls')),
    url(r'^leads/', include('v0.ui.mis.urls')),
    url(r'^b2b/', include('v0.ui.b2b.urls')),
    url(r'^bot/', include('v0.ui.bot.urls')),

    # Script urls
    url(r'^scripts/', include(('v0.scripts.urls'))),

    # url(r'^website/create_business/load_business_types/',web_views.getBusinessTypesAPIView.as_view()),
    # url(r'^website/subtypes/(?P<id>[A-Z_a-z0-9]+)/$', web_views.getBusinessSubTypesAPIView.as_view()),

    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/tower/$', views.TowerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/flat/$', views.FlatTypeAPIView.as_view()),
    #url(r'^society/(?P<id>[A-Z_a-z0-9]+)/tower/(?P<tower_id>[A-Z_a-z0-9]+)$', views.TowerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)$', SocietyAPIView.as_view()),
    url(r'^society/$', SocietyAPIView.as_view()),
    # url(r'^society/list/$', views.SocietyAPIListView.as_view()),
    url(r'^society/list/$', SocietyList.as_view()),
    url(r'^society/list/by/number/$', SocietyListByNumber.as_view()),

    url(r'^busshelter/list/$', BusShelter.as_view()),
    url(r'^busshelter/search/$', BusShelterSearchView.as_view()),
    url(r'^society/filter/$', SocietyAPIFiltersView.as_view()),
    url(r'^society/filterList/$', SocietyAPIFiltersListView.as_view()),
    url(r'^society/filterSubArea/$',views.SocietyAPIFilterSubAreaView.as_view(),),
    url(r'^societyList/sortedSocieties/$', SocietyAPISortedListView.as_view()),
    url(r'^society/societyIds/$', SocietyAPISocietyIdsView.as_view()),

    #url(r'^society/(?P<id>[A-Z_a-z0-9]+)/car_display/$', views.CarDisplayAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/other_inventory/$', views.OtherInventoryAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/events/$', views.EventAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/inventory_summary/$', views.InventorySummaryAPIView.as_view(), name='inventory-summary'),
    url(r'^society/save-summary-data/$', views.ImportSummaryData.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/basic_pricing/$', views.BasicPricingAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/fliers/$', views.FlierAPIView.as_view()),
    #url(r'^society/(?P<id>[A-Z_a-z0-9]+)/posters/$', views.PosterAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/standee_banners/$', views.StandeeBannerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/stalls/$', views.StallAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/inventory_pricing/$', views.InventoryPricingAPIView.as_view()),

    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/image_locations/$', views.ImageLocationsAPIView.as_view()),

    url(r'^create_supplier/load_initial_data/$', views.GetInitialDataAPIView.as_view()),
    url(r'^(?P<id>[A-Z_a-z0-9]+)/load_initial_data_corporate/$', SaveBasicCorporateDetailsAPIView.as_view(), name='load-initial-corporate-data'),
    url(r'^locations/(?P<id>[A-Z_a-z0-9]+)/$', views.LocationsAPIView.as_view(), name='locations'),
    
    url(r'^getCityArea$', views.getCityAreaAPIView.as_view(), name='getCityArea'),
    url(r'^bulk-locations/$', views.AddBulkLocationAPIView.as_view(), name='locations'),
    url(r'^supplier/generate_id/$', GenerateSupplierIdAPIView.as_view(), name='generate-id'),
    url(r'^check_supplier_code/(?P<code>[A-Z0-9]+)$', checkSupplierCodeAPIView.as_view()),

    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/posters/$', views.PosterAPIView.as_view()),

    url(r'^user_profiles/$', views.UsersProfilesAPIView.as_view()),
    url(r'^user_profiles/(?P<id>[A-Z_a-z0-9]+)$', views.getUserData.as_view()),
    url(r'^users/delete/$', views.deleteUsersAPIView.as_view()),
   
    url(r'^setResetPassword$', views.setResetPasswordAPIView.as_view()),

    url(r'^forgotPassword$', views.forgotPasswordAPIView.as_view()),
    url(r'^getHeaderData$', views.getHeaderDataAPIView.as_view(), name='getHeaderData'),

    url(r'^corporate/(?P<id>[A-Z_a-z0-9]+)/save_basic_corporate_details$', SaveBasicCorporateDetailsAPIView.as_view()),
    # url(r'^corporate/(?P<id>[A-Z_a-z0-9]+)/save_contact_details$', views.ContactDetailsGenericAPIView.as_view()),
    # url(r'^corporate/save_basic_corporate_details$', views.saveBasicCorporateDetailsAPIView.as_view())
    url(r'^corporate/(?P<id>[A-Z_a-z0-9]+)/save_building_details$', SaveBuildingDetailsAPIView.as_view(), name='save-building-details'),
    url(r'^corporate/(?P<id>[A-Z_a-z0-9]+)/get_company_list$', CompanyDetailsAPIView.as_view(), name='get-corporate-company-list'),
    url(r'^corporate/(?P<id>[A-Z_a-z0-9]+)/save_company_details$', CorporateCompanyDetailsAPIView.as_view(), name='save-company-details'),
    url(r'^corporate/(?P<id>[A-Z_a-z0-9]+)/get_company_data$', CorporateCompanyDetailsAPIView.as_view(), name='get-company-data'),

    url(r'^salon/(?P<id>[A-Z_a-z0-9]+)/save_basic_salon_details$', saveBasicSalonDetailsAPIView.as_view()),
    url(r'^(?P<id>[A-Z_a-z0-9]+)/load_initial_data_salon/$', saveBasicSalonDetailsAPIView.as_view()),

    url(r'^gym/(?P<id>[A-Z_a-z0-9]+)/save_basic_gym_details$', saveBasicGymDetailsAPIView.as_view()),
    url(r'^(?P<id>[A-Z_a-z0-9]+)/load_initial_data_gym/$', saveBasicGymDetailsAPIView.as_view()),

    url(r'^(?P<id>[A-Z_a-z0-9]+)/bus-shelter/$', BusShelter.as_view()),
    url(r'^(?P<id>[A-Z_a-z0-9]+)/get-bus-shelter/$', getBusShelter.as_view()),

    url(r'^suppliers-meta/$', SuppliersMeta.as_view()),
    url(r'^suppliers-meta-data/$', SuppliersMetaData.as_view()),
    url(r'^supplier/(?P<id>[A-Z_a-z0-9]+)/image_details/$', SupplierImageDetails.as_view()),
    url(r'^import_society_payment_details/$', views.ImportSocietyPaymentDetails.as_view()),
    url(r'^supplier/society-data-import-excel/$', SocietyDataImport.as_view()),
    url(r'^supplier/corporate-park-data-import-excel/$', CorporateParkDataImport.as_view()),
]


router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'^supplier-generic', SupplierGenericViewSet, base_name='supplier-generic')
router.register(r'^event', views.EventViewSet, base_name='event')
router.register(r'^corporate', CorporateViewSet, base_name='corporate')
router.register(r'^gym', GymViewSet, base_name='gym')
router.register(r'^salon', SalonViewSet, base_name='salon')
router.register(r'^retail-shop', RetailShopViewSet, base_name='retail-shop')
router.register(r'^image-mapping', views.ImageMappingViewSet, base_name='image-mapping')
router.register(r'^state', views.StateViewSet, base_name='state')
router.register(r'^bus-depot', BusDepotViewSet, base_name='bus-depot')

router.register(r'^educational-institute', EducationalInstituteViewSet, base_name='educational-institute')

router.register(r'^hording', HordingViewSet, base_name='hording')



urlpatterns += router.urls


