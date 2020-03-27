from __future__ import absolute_import
from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^society-analytics/', GetSocietyAnalytics.as_view()),
    url(r'^campaign-analytics/', GetCampaignWiseAnalytics.as_view()),
    url(r'^campaign/supplier-analytics/', GetSupplierDetail.as_view()),
    url(r'^campaign/supplier-count/', GetCampaignStatusCount.as_view()),
    url(r'^user-analytics-today/', GetUserAssignedSuppliersDetailTillToday.as_view()),
]
