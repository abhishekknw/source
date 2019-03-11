from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (BaseBookingTemplateView, BookingTemplateView, BookingTemplateById, BaseBookingTemplateById)

urlpatterns = [
    url(r'^base-booking-template/$', BaseBookingTemplateView.as_view()),
    url(r'^base-booking-template/(?P<base_booking_template_id>[A-Z_a-z0-9]+)/$', BaseBookingTemplateById.as_view()),
    url(r'^booking-template/$', BookingTemplateView.as_view()),
    url(r'^booking-template/(?P<booking_template_id>[A-Z_a-z0-9]+)/$', BookingTemplateById.as_view())

]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
