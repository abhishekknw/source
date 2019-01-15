from __future__ import absolute_import
from django.conf.urls import url
from .views import (GetLeadsDataGeneric, AnalyticSavedOperators)

urlpatterns = [
    url(r'^get-leads-data-generic/$', GetLeadsDataGeneric.as_view()),
    url(r'^metrics/$', AnalyticSavedOperators.as_view()),
    #url(r'^analytics-sets/$', AnalyticSavedSets.as_view()),
]