from django.conf.urls import url
from views import LeadsViewSetExcel, CreateLeadsForm, GetLeadsForm,LeadsFormEntry, GetLeadsEntries

urlpatterns = [
    url(r'^create-leads-excel/$', LeadsViewSetExcel.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/create$', CreateLeadsForm.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/form$', GetLeadsForm.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/insert_lead$', LeadsFormEntry.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/entry_list/(?P<supplier_id>[A-Z_a-z0-9]+)$', GetLeadsEntries.as_view()),
]