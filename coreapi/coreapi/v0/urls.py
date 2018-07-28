from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from v0 import views
from v0.ui.inventory.views import AssignInventories, BannerInventoryAPIView, BannerInventoryAPIListView, \
    CreateAdInventoryTypeDurationType, InventoryInfoAPIView, InventoryInfoAPIListView, PoleInventoryAPIView, \
    PoleInventoryAPIListView, PosterInventoryAPIView, PosterInventoryAPIListView, PosterInventoryMappingAPIView, \
    PosterInventoryMappingAPIListView, StandeeInventoryAPIView, StandeeInventoryAPIListView,  \
    StallInventoryAPIView, StallInventoryAPIListView, StreetFurnitureAPIView, StreetFurnitureAPIListView, \
    WallInventoryAPIView, WallInventoryAPIListView

from v0.ui.supplier.views import SupplierInfoAPIView, SupplierInfoAPIListView, SupplierTypeSocietyAPIView, \
    SupplierTypeSocietyAPIListView


urlpatterns = [
    url(r'^ui/', include('v0.ui.urls')),
    url(r'^android/', include('v0.android.urls')),
    url(r'^bannerinventory/(?P<id>[0-9]+)$', BannerInventoryAPIView.as_view()),
    url(r'^bannerinventory/$', BannerInventoryAPIListView.as_view()),
    url(r'^communityhallinfo/(?P<id>[0-9]+)$', views.CommunityHallInfoAPIView.as_view()),
    url(r'^communityhallinfo/$', views.CommunityHallInfoAPIListView.as_view()),
    url(r'^doortodoorinfo/(?P<id>[0-9]+)$', views.DoorToDoorInfoAPIView.as_view()),
    url(r'^doortodoorinfo/$', views.DoorToDoorInfoAPIListView.as_view()),
    url(r'^liftdetails/(?P<id>[0-9]+)$', views.LiftDetailsAPIView.as_view()),
    url(r'^liftdetails/$', views.LiftDetailsAPIListView.as_view()),
    url(r'^noticeboarddetails/(?P<id>[0-9]+)$', views.NoticeBoardDetailsAPIView.as_view()),
    url(r'^noticeboarddetails/$', views.NoticeBoardDetailsAPIListView.as_view()),
    url(r'^posterinventory/(?P<id>[0-9]+)$', PosterInventoryAPIView.as_view()),
    url(r'^posterinventory/$', PosterInventoryAPIListView.as_view()),
    url(r'^societyflat/(?P<id>[0-9]+)$', views.SocietyFlatAPIView.as_view()),
    url(r'^societyflat/$', views.SocietyFlatAPIListView.as_view()),
    url(r'^standeeinventory/(?P<id>[0-9]+)$', StandeeInventoryAPIView.as_view()),
    url(r'^standeeinventory/$', StandeeInventoryAPIListView.as_view()),
    url(r'^swimmingpoolinfo/(?P<id>[0-9]+)$', views.SwimmingPoolInfoAPIView.as_view()),
    url(r'^swimmingpoolinfo/$', views.SwimmingPoolInfoAPIListView.as_view()),
    url(r'^wallinventory/(?P<id>[0-9]+)$', WallInventoryAPIView.as_view()),
    url(r'^wallinventory/$', WallInventoryAPIListView.as_view()),
    url(r'^userinquiry/(?P<id>[0-9]+)$', views.UserInquiryAPIView.as_view()),
    url(r'^userinquiry/$', views.UserInquiryAPIListView.as_view()),
    url(r'^commonareadetails/(?P<id>[0-9]+)$', views.CommonAreaDetailsAPIView.as_view()),
    url(r'^commonareadetails/$', views.CommonAreaDetailsAPIListView.as_view()),

    url(r'^contactdetails/(?P<id>[0-9]+)$', views.ContactDetailsAPIView.as_view()),
    url(r'^contactdetails/$', views.ContactDetailsAPIListView.as_view()),

    url(r'^events/(?P<id>[0-9]+)$', views.EventsAPIView.as_view()),
    url(r'^events/$', views.EventsAPIListView.as_view()),

    url(r'^inventoryinfo/(?P<id>[0-9]+)$', InventoryInfoAPIView.as_view()),
    url(r'^inventoryinfo/$', InventoryInfoAPIListView.as_view()),

    url(r'^mailboxinfo/(?P<id>[0-9]+)$', views.MailboxInfoAPIView.as_view()),
    url(r'^mailboxinfo/$', views.MailboxInfoAPIListView.as_view()),

    url(r'^operationsinfo/(?P<id>[0-9]+)$', views.OperationsInfoAPIView.as_view()),
    url(r'^operationsinfo/$', views.OperationsInfoAPIListView.as_view()),

    url(r'^poleinventory/(?P<id>[0-9]+)$', PoleInventoryAPIView.as_view()),
    url(r'^poleinventory/$', PoleInventoryAPIListView.as_view()),

    url(r'^posterinventorymapping/(?P<id>[0-9]+)$', PosterInventoryMappingAPIView.as_view()),
    url(r'^posterinventorymapping/$', PosterInventoryMappingAPIListView.as_view()),

    url(r'^ratiodetails/(?P<id>[0-9]+)$', views.RatioDetailsAPIView.as_view()),
    url(r'^ratiodetails/$', views.RatioDetailsAPIListView.as_view()),

    url(r'^signup/(?P<id>[0-9]+)$', views.SignupAPIView.as_view()),
    url(r'^signup/$', views.SignupAPIListView.as_view()),

    url(r'^stallinventory/(?P<id>[0-9]+)$', StallInventoryAPIView.as_view()),
    url(r'^stallinventory/$', StallInventoryAPIListView.as_view()),

    url(r'^streetfurniture/(?P<id>[0-9]+)$', StreetFurnitureAPIView.as_view()),
    url(r'^streetfurniture/$', StreetFurnitureAPIListView.as_view()),

    url(r'^supplierinfo/(?P<id>[0-9]+)$', SupplierInfoAPIView.as_view()),
    url(r'^supplierinfo/$', SupplierInfoAPIListView.as_view()),

    url(r'^suppliertypesociety/(?P<id>[A-Za-z0-9]+)$', SupplierTypeSocietyAPIView.as_view()),
    url(r'^suppliertypesociety/$', SupplierTypeSocietyAPIListView.as_view()),

    url(r'^societytower/(?P<id>[0-9]+)$', views.SocietyTowerAPIView.as_view()),
    url(r'^societytower/$', views.SocietyTowerAPIListView.as_view()),

    url(r'^flat/(?P<id>[0-9]+)$', views.FlatTypeAPIView.as_view()),
    url(r'^flat/$', views.FlatTypeAPIListView.as_view()),
    url(r'^populate-content-types/$', views.PopulateContentTypeFields.as_view()),
    url(r'^set-user-to-master-user/$', views.SetUserToMasterUser.as_view()),
    url(r'^create-society-test-data/$', views.CreateSocietyTestData.as_view()),
    url(r'^create-business-type-subtypes/$', views.CreateBusinessTypeSubType.as_view()),
    url(r'^create-adinventory-duration-types/$', CreateAdInventoryTypeDurationType.as_view()),
    url(r'^assign-inventories/$', AssignInventories.as_view()),
    url(r'^set-inventory-pricing/$', views.SetInventoryPricing.as_view()),
    url(r'^populate-amenities/$', views.PopulateAmenities.as_view()),
    url(r'^guest-user/$', views.GuestUser.as_view()),
    url(r'^set-params/$', views.SetParams.as_view()),
    url(r'^copy-organisations/$', views.CopyOrganisation.as_view())
    ]

# adding urls for Permission View Set
router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'permission', views.PermissionsViewSet, base_name='permission')
router.register(r'^user', views.UserViewSet, base_name='user')
router.register(r'^group', views.GroupViewSet, base_name='group')
urlpatterns += router.urls
