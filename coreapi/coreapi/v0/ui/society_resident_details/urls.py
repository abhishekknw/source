from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import UpdateResident, CreateUserResident, GetResidentCount


urlpatterns = [
    url(r'^user-mapping/', UpdateResident.as_view()),
    url(r'^user-resident/', CreateUserResident.as_view()),
    url(r'^resident-count/', GetResidentCount.as_view())
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls