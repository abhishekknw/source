from django.conf.urls import include, url
from v0.ui import views

urlpatterns = [
    url(r'^society/(?P<id>[A-Za-z0-9]+)/tower/$', views.TowerAPIView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)$', views.SocietyAPIView.as_view()),
    url(r'^society/$', views.SocietyAPIListView.as_view()),
    url(r'^society/(?P<id>[A-Za-z0-9]+)/events/$', views.EventAPIView.as_view()),

]
