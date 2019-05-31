from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    url(r'^state/$', State.as_view()),
    url(r'^state/(?P<state_id>[A-Z_a-z0-9]+)/$', StateById.as_view()),
    url(r'^city/$', City.as_view()),
    url(r'^city/(?P<city_id>[A-Z_a-z0-9]+)/$', CityById.as_view()),
    url(r'^area/$', Area.as_view()),
    url(r'^area/(?P<area_id>[A-Z_a-z0-9]+)/$', AreaById.as_view()),
    url(r'^sub-area/$', SubArea.as_view()),
    url(r'^sub-area/(?P<sub_area_id>[A-Z_a-z0-9]+)/$', SubAreaById.as_view()),

]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls