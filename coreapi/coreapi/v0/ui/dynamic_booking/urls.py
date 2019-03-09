from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
=======
from .views import (BaseBookingTemplateView, BookingTemplateView, BookingTemplateById, BaseBookingTemplateById)
>>>>>>> dev-server

urlpatterns = [
    url(r'^base-booking-template/$', BaseBookingTemplateView.as_view()),
    url(r'^base-booking-template/(?P<base_booking_template_id>[A-Z_a-z0-9]+)/$', BaseBookingTemplateById.as_view()),
    url(r'^booking-template/$', BookingTemplateView.as_view()),
<<<<<<< HEAD
=======
    url(r'^booking-template/(?P<booking_template_id>[A-Z_a-z0-9]+)/$', BookingTemplateById.as_view())
>>>>>>> dev-server
]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
