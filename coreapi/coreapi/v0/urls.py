from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

from v0 import views


urlpatterns = patterns('',
    url(r'^ui/', include('v0.ui.urls')),
    url(r'^android/', include('v0.android.urls')),
    url(r'^bannerinventory/(?P<id>[0-9]+)$', views.BannerInventoryAPIView.as_view()),
    url(r'^bannerinventory/$', views.BannerInventoryAPIListView.as_view()),
    url(r'^communityhallinfo/(?P<id>[0-9]+)$', views.CommunityHallInfoAPIView.as_view()),
    url(r'^communityhallinfo/$', views.CommunityHallInfoAPIListView.as_view()),
    url(r'^doortodoorinfo/(?P<id>[0-9]+)$', views.DoorToDoorInfoAPIView.as_view()),
    url(r'^doortodoorinfo/$', views.DoorToDoorInfoAPIListView.as_view()),
    url(r'^liftdetails/(?P<id>[0-9]+)$', views.LiftDetailsAPIView.as_view()),
    url(r'^liftdetails/$', views.LiftDetailsAPIListView.as_view()),
    url(r'^noticeboarddetails/(?P<id>[0-9]+)$', views.NoticeBoardDetailsAPIView.as_view()),
    url(r'^noticeboarddetails/$', views.NoticeBoardDetailsAPIListView.as_view()),
    url(r'^posterinventory/(?P<id>[0-9]+)$', views.PosterInventoryAPIView.as_view()),
    url(r'^posterinventory/$', views.PosterInventoryAPIListView.as_view()),
    url(r'^societyflat/(?P<id>[0-9]+)$', views.SocietyFlatAPIView.as_view()),
    url(r'^societyflat/$', views.SocietyFlatAPIListView.as_view()),
    url(r'^standeeinventory/(?P<id>[0-9]+)$', views.StandeeInventoryAPIView.as_view()),
    url(r'^standeeinventory/$', views.StandeeInventoryAPIListView.as_view()),
    url(r'^swimmingpoolinfo/(?P<id>[0-9]+)$', views.SwimmingPoolInfoAPIView.as_view()),
    url(r'^swimmingpoolinfo/$', views.SwimmingPoolInfoAPIListView.as_view()),
    url(r'^wallinventory/(?P<id>[0-9]+)$', views.WallInventoryAPIView.as_view()),
    url(r'^wallinventory/$', views.WallInventoryAPIListView.as_view()),
    url(r'^userinquiry/(?P<id>[0-9]+)$', views.UserInquiryAPIView.as_view()),
    url(r'^userinquiry/$', views.UserInquiryAPIListView.as_view()),
    url(r'^commonareadetails/(?P<id>[0-9]+)$', views.CommonAreaDetailsAPIView.as_view()),
    url(r'^commonareadetails/$', views.CommonAreaDetailsAPIListView.as_view()),

    url(r'^contactdetails/(?P<id>[0-9]+)$', views.ContactDetailsAPIView.as_view()),
    url(r'^contactdetails/$', views.ContactDetailsAPIListView.as_view()),

    url(r'^events/(?P<id>[0-9]+)$', views.EventsAPIView.as_view()),
    url(r'^events/$', views.EventsAPIListView.as_view()),

    url(r'^inventoryinfo/(?P<id>[0-9]+)$', views.InventoryInfoAPIView.as_view()),
    url(r'^inventoryinfo/$', views.InventoryInfoAPIListView.as_view()),

    url(r'^mailboxinfo/(?P<id>[0-9]+)$', views.MailboxInfoAPIView.as_view()),
    url(r'^mailboxinfo/$', views.MailboxInfoAPIListView.as_view()),

    url(r'^operationsinfo/(?P<id>[0-9]+)$', views.OperationsInfoAPIView.as_view()),
    url(r'^operationsinfo/$', views.OperationsInfoAPIListView.as_view()),

    url(r'^poleinventory/(?P<id>[0-9]+)$', views.PoleInventoryAPIView.as_view()),
    url(r'^poleinventory/$', views.PoleInventoryAPIListView.as_view()),

    url(r'^posterinventorymapping/(?P<id>[0-9]+)$', views.PosterInventoryMappingAPIView.as_view()),
    url(r'^posterinventorymapping/$', views.PosterInventoryMappingAPIListView.as_view()),

    url(r'^ratiodetails/(?P<id>[0-9]+)$', views.RatioDetailsAPIView.as_view()),
    url(r'^ratiodetails/$', views.RatioDetailsAPIListView.as_view()),

    url(r'^signup/(?P<id>[0-9]+)$', views.SignupAPIView.as_view()),
    url(r'^signup/$', views.SignupAPIListView.as_view()),

    url(r'^stallinventory/(?P<id>[0-9]+)$', views.StallInventoryAPIView.as_view()),
    url(r'^stallinventory/$', views.StallInventoryAPIListView.as_view()),

    url(r'^streetfurniture/(?P<id>[0-9]+)$', views.StreetFurnitureAPIView.as_view()),
    url(r'^streetfurniture/$', views.StreetFurnitureAPIListView.as_view()),

    url(r'^supplierinfo/(?P<id>[0-9]+)$', views.SupplierInfoAPIView.as_view()),
    url(r'^supplierinfo/$', views.SupplierInfoAPIListView.as_view()),

    url(r'^suppliertypesociety/(?P<id>[A-Za-z0-9]+)$', views.SupplierTypeSocietyAPIView.as_view()),
    url(r'^suppliertypesociety/$', views.SupplierTypeSocietyAPIListView.as_view()),

    url(r'^societytower/(?P<id>[0-9]+)$', views.SocietyTowerAPIView.as_view()),
    url(r'^societytower/$', views.SocietyTowerAPIListView.as_view()),

    url(r'^flat/(?P<id>[0-9]+)$', views.FlatTypeAPIView.as_view()),
    url(r'^flat/$', views.FlatTypeAPIListView.as_view()),
    url(r'^populate-content-types/$', views.PopulateContentTypeFields.as_view()),
    url(r'^set-user-to-master-user/$', views.SetUserToMasterUser.as_view()),


)

# adding urls for Permission View Set
router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'permission', views.PermissionsViewSet, base_name='permission')
urlpatterns += router.urls