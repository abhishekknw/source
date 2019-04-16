from __future__ import absolute_import
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import (BaseBookingTemplateView, BookingTemplateView, BookingTemplateById, BaseBookingTemplateById,
                     BookingDataView, BookingDataById, BookingDataByCampaignId, BookingDetailsView, BookingDetailsById,
                    BookingDetailsByCampaignId, BookingAssignment)

urlpatterns = [
    url(r'^base-booking-template/$', BaseBookingTemplateView.as_view()),
    url(r'^base-booking-template/(?P<base_booking_template_id>[A-Z_a-z0-9]+)/$', BaseBookingTemplateById.as_view()),
    url(r'^booking-template/$', BookingTemplateView.as_view()),
    url(r'^booking-template/(?P<booking_template_id>[A-Z_a-z0-9]+)/$', BookingTemplateById.as_view()),
    url(r'^booking-data/$', BookingDataView.as_view()),
    url(r'^booking-data/(?P<booking_data_id>[A-Z_a-z0-9]+)/$', BookingDataById.as_view()),
    url(r'^booking-data/campaign/(?P<campaign_id>[A-Z_a-z0-9]+)/$', BookingDataByCampaignId.as_view()),
    url(r'^booking-details/$', BookingDetailsView.as_view()),
    url(r'^booking-details/(?P<booking_details_id>[A-Z_a-z0-9]+)/$', BookingDetailsById.as_view()),
    url(r'^booking-details/campaign/(?P<campaign_id>[A-Z_a-z0-9]+)/$', BookingDetailsByCampaignId.as_view()),
    url(r'^booking-assignment/$', BookingAssignment.as_view()),

]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
