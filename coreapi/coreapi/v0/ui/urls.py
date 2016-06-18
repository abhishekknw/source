from django.conf.urls import include, url
from v0.ui import views

urlpatterns = [

    url(r'^website/', include('v0.ui.website.urls')),

    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/tower/$', views.TowerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/flat/$', views.FlatTypeAPIView.as_view()),
    #url(r'^society/(?P<id>[A-Z_a-z0-9]+)/tower/(?P<tower_id>[A-Z_a-z0-9]+)$', views.TowerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)$', views.SocietyAPIView.as_view()),
    url(r'^society/$', views.SocietyAPIView.as_view()),
    url(r'^society/list/$', views.SocietyAPIListView.as_view()),
    url(r'^society/filter/$', views.SocietyAPIFiltersView.as_view()),
    url(r'^society/filterList/$', views.SocietyAPIFiltersListView.as_view()),

    #url(r'^society/(?P<id>[A-Z_a-z0-9]+)/car_display/$', views.CarDisplayAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/other_inventory/$', views.OtherInventoryAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/events/$', views.EventAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/inventory_summary/$', views.InventorySummaryAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/basic_pricing/$', views.BasicPricingAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/fliers/$', views.FlierAPIView.as_view()),
    #url(r'^society/(?P<id>[A-Z_a-z0-9]+)/posters/$', views.PosterAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/standee_banners/$', views.StandeeBannerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/stalls/$', views.StallAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/inventory_pricing/$', views.InventoryPricingAPIView.as_view()),

    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/image_locations/$', views.ImageLocationsAPIView.as_view()),
    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/image_mapping/$', views.ImageMappingAPIView.as_view()),

    url(r'^create_supplier/load_initial_data/$', views.getInitialDataAPIView.as_view()),
    url(r'^locations/(?P<id>[A-Z_a-z0-9]+)/$', views.getLocationsAPIView.as_view()),
    url(r'^supplier/generate_id/$', views.generateSupplierIdAPIView.as_view()),
    url(r'^check_supplier_code/(?P<code>[A-Z0-9]+)$', views.checkSupplierCodeAPIView.as_view()),

    url(r'^society/(?P<id>[A-Z_a-z0-9]+)/posters/$', views.PosterAPIView.as_view()),

    url(r'^user_profiles/$', views.UsersProfilesAPIView.as_view()),
    url(r'^user_profiles/(?P<id>[A-Z_a-z0-9]+)$', views.getUserData.as_view()),
    url(r'^users/delete/$', views.deleteUsersAPIView.as_view()),


]
