from django.conf.urls import patterns, include, url
from django.contrib import admin
from v0 import views


urlpatterns = patterns('',
    url(r'^ui/', include('v0.ui.urls')),

    url(r'^masterbannerinventory/(?P<id>[0-9]+)$', views.MasterBannerInventoryAPIView.as_view()),
    url(r'^masterbannerinventory/$', views.MasterBannerInventoryAPIListView.as_view()),

    url(r'^mastercardisplayinventory/(?P<id>[0-9]+)$', views.MasterCarDisplayInventoryAPIView.as_view()),
    url(r'^mastercardisplayinventory/$', views.MasterCarDisplayInventoryAPIListView.as_view()),

    url(r'^mastercommunityhallinfo/(?P<id>[0-9]+)$', views.MasterCommunityHallInfoAPIView.as_view()),
    url(r'^mastercommunityhallinfo/$', views.MasterCommunityHallInfoAPIListView.as_view()),

    url(r'^masterdoortodoorinfo/(?P<id>[0-9]+)$', views.MasterDoorToDoorInfoAPIView.as_view()),
    url(r'^masterdoortodoorinfo/$', views.MasterDoorToDoorInfoAPIListView.as_view()),

    url(r'^masterliftdetails/(?P<id>[0-9]+)$', views.MasterLiftDetailsAPIView.as_view()),
    url(r'^masterliftdetails/$', views.MasterLiftDetailsAPIListView.as_view()),

    url(r'^masternoticeboarddetails/(?P<id>[0-9]+)$', views.MasterNoticeBoardDetailsAPIView.as_view()),
    url(r'^masternoticeboarddetails/$', views.MasterNoticeBoardDetailsAPIListView.as_view()),

    url(r'^masterposterinventory/(?P<id>[0-9]+)$', views.MasterPosterInventoryAPIView.as_view()),
    url(r'^masterposterinventory/$', views.MasterPosterInventoryAPIListView.as_view()),

    url(r'^mastersocietyflat/(?P<id>[0-9]+)$', views.MasterSocietyFlatAPIView.as_view()),
    url(r'^mastersocietyflat/$', views.MasterSocietyFlatAPIListView.as_view()),

    url(r'^masterstandeeinventory/(?P<id>[0-9]+)$', views.MasterStandeeInventoryAPIView.as_view()),
    url(r'^masterstandeeinventory/$', views.MasterStandeeInventoryAPIListView.as_view()),

    url(r'^masterswimmingpoolinfo/(?P<id>[0-9]+)$', views.MasterSwimmingPoolInfoAPIView.as_view()),
    url(r'^masterswimmingpoolinfo/$', views.MasterSwimmingPoolInfoAPIListView.as_view()),

    url(r'^masterwallinventory/(?P<id>[0-9]+)$', views.MasterWallInventoryAPIView.as_view()),
    url(r'^masterwallinventory/$', views.MasterWallInventoryAPIListView.as_view()),

    url(r'^userinquiry/(?P<id>[0-9]+)$', views.UserInquiryAPIView.as_view()),
    url(r'^userinquiry/$', views.UserInquiryAPIListView.as_view()),

    url(r'^commonareadetails/(?P<id>[0-9]+)$', views.CommonAreaDetailsAPIView.as_view()),
    url(r'^commonareadetails/$', views.CommonAreaDetailsAPIListView.as_view()),

    url(r'^mastercontactdetails/(?P<id>[0-9]+)$', views.MasterContactDetailsAPIView.as_view()),
    url(r'^mastercontactdetails/$', views.MasterContactDetailsAPIListView.as_view()),

    url(r'^masterevents/(?P<id>[0-9]+)$', views.MasterEventsAPIView.as_view()),
    url(r'^masterevents/$', views.MasterEventsAPIListView.as_view()),

    url(r'^masterinventoryinfo/(?P<id>[0-9]+)$', views.MasterInventoryInfoAPIView.as_view()),
    url(r'^masterinventoryinfo/$', views.MasterInventoryInfoAPIListView.as_view()),

    url(r'^mastermailboxinfo/(?P<id>[0-9]+)$', views.MasterMailboxInfoAPIView.as_view()),
    url(r'^mastermailboxinfo/$', views.MasterMailboxInfoAPIListView.as_view()),

    url(r'^masteroperationsinfo/(?P<id>[0-9]+)$', views.MasterOperationsInfoAPIView.as_view()),
    url(r'^masteroperationsinfo/$', views.MasterOperationsInfoAPIListView.as_view()),

    url(r'^masterpoleinventory/(?P<id>[0-9]+)$', views.MasterPoleInventoryAPIView.as_view()),
    url(r'^masterpoleinventory/$', views.MasterPoleInventoryAPIListView.as_view()),

    url(r'^masterposterinventorymapping/(?P<id>[0-9]+)$', views.MasterPosterInventoryMappingAPIView.as_view()),
    url(r'^masterposterinventorymapping/$', views.MasterPosterInventoryMappingAPIListView.as_view()),

    url(r'^masterratiodetails/(?P<id>[0-9]+)$', views.MasterRatioDetailsAPIView.as_view()),
    url(r'^masterratiodetails/$', views.MasterRatioDetailsAPIListView.as_view()),

    url(r'^mastersignup/(?P<id>[0-9]+)$', views.MasterSignupAPIView.as_view()),
    url(r'^mastersignup/$', views.MasterSignupAPIListView.as_view()),

    url(r'^masterstallinventory/(?P<id>[0-9]+)$', views.MasterStallInventoryAPIView.as_view()),
    url(r'^masterstallinventory/$', views.MasterStallInventoryAPIListView.as_view()),

    url(r'^masterstreetfurniture/(?P<id>[0-9]+)$', views.MasterStreetFurnitureAPIView.as_view()),
    url(r'^masterstreetfurniture/$', views.MasterStreetFurnitureAPIListView.as_view()),

    url(r'^mastersupplierinfo/(?P<id>[0-9]+)$', views.MasterSupplierInfoAPIView.as_view()),
    url(r'^mastersupplierinfo/$', views.MasterSupplierInfoAPIListView.as_view()),

    url(r'^mastersuppliertypesociety/(?P<id>[A-Za-z0-9]+)$', views.MasterSupplierTypeSocietyAPIView.as_view()),
    url(r'^mastersuppliertypesociety/$', views.MasterSupplierTypeSocietyAPIListView.as_view()),

    url(r'^mastersuppliertypesocietytower/(?P<id>[0-9]+)$', views.MasterSupplierTypeSocietyTowerAPIView.as_view()),
    url(r'^mastersuppliertypesocietytower/$', views.MasterSupplierTypeSocietyTowerAPIListView.as_view()),

)
