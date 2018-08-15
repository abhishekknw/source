from django.conf.urls import url
from views import LeadsViewSetExcel, CreateLeadsForm

urlpatterns = [
    url(r'^create-leads-excel/$', LeadsViewSetExcel.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/create$', CreateLeadsForm.as_view())
]