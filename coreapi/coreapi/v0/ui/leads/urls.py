from django.conf.urls import url
from v0.ui.website.views import LeadsViewSetExcel

urlpatterns = [
    url(r'^create-leads-excel/$', LeadsViewSetExcel.as_view())
]