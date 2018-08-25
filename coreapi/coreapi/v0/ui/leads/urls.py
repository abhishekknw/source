from django.conf.urls import url
from views import (CreateLeadsForm, GetLeadsForm, LeadsFormEntry, GetLeadsEntries,
                   LeadsFormBulkEntry, GenerateLeadForm, DeleteLeadItems, DeleteLeadForm, DeleteLeadEntry,
                   LeadFormUpdate)

urlpatterns = [
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/create$', CreateLeadsForm.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/form$', GetLeadsForm.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/insert_lead$', LeadsFormEntry.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/entry_list/(?P<supplier_id>[A-Z_a-z0-9]+)$', GetLeadsEntries.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/import_lead$', LeadsFormBulkEntry.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/generate_lead_form$', GenerateLeadForm.as_view()),
    url(r'^(?P<form_id>[A-Z_a-z0-9]+)/delete_form_element/(?P<item_id>[A-Z_a-z0-9]+)$', DeleteLeadItems.as_view()),
    url(r'^(?P<form_id>[A-Z_a-z0-9]+)/delete_form$', DeleteLeadForm.as_view()),
    url(r'^(?P<form_id>[A-Z_a-z0-9]+)/delete_entry/(?P<entry_id>[A-Z_a-z0-9]+)$', DeleteLeadEntry.as_view()),
    url(r'^(?P<form_id>[A-Z_a-z0-9]+)/add_field$', LeadFormUpdate.as_view()),
]