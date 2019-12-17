from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    url(r'^society-analytics/', GetSocietyAnalytics.as_view()),
    url(r'^campaign-analytics/', GetCampaignWiseAnalytics.as_view()),
    url(r'^campaign/supplier-analytics/', GetSupplierDetail.as_view()),
    url(r'^campaign/supplier-count/', GetCampaignStatusCount.as_view()),
    url(r'^user-analytics-today/', GetUserAssignedSuppliersDetailTillToday.as_view())
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
