from django.conf.urls import include, url
from v0.ui import views

urlpatterns = [
    url(r'^society/(?P<id>[A-Za-z0-9]+)/tower/$', views.TowerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)$', views.SocietyAPIView.as_view()),
    url(r'^society/$', views.SocietyAPIListView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)/car_display/$', views.CarDisplayAPIView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)/other_inventory/$', views.OtherInventoryAPIView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)/events/$', views.EventAPIView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)/basic_pricing/$', views.BasicPricingAPIView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)/standee_banners/$', views.StandeeBannerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)/stalls/$', views.StallAPIView.as_view()),

]
