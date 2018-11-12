from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (CreateLeadsForm, GetLeadsForm, LeadsFormEntry, GetLeadsEntries, GetLeadsEntriesBySupplier,
                   LeadsFormBulkEntry, GenerateLeadForm, DeleteLeadForm, DeleteLeadEntry,
                   SmsContact, EditLeadsData, AddLeadFormItems, EditLeadsForm,
                   LeadsSummary, GetLeadsEntriesByCampaignId, GenerateLeadDataExcel,
                   SanitizeLeadsData, GenerateDemoData, UpdateLeadsDataSHA256, UpdateGlobalHotLeadCriteria,
                   UpdateLeadsDataIsHot)
from old_scripts import MigrateLeadsToMongo

urlpatterns = [
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/create$', CreateLeadsForm.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/form$', GetLeadsForm.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/insert_lead$', LeadsFormEntry.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/entry_list/(?P<supplier_id>[A-Z_a-z0-9]+)$', GetLeadsEntriesBySupplier.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/entry_list/$', GetLeadsEntries.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/entry_list_by_campaign_id$', GetLeadsEntriesByCampaignId.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/import_lead$', LeadsFormBulkEntry.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/generate_lead_form$', GenerateLeadForm.as_view()),
    url(r'^(?P<leads_form_id>[A-Z_a-z0-9]+)/generate_lead_data_excel', GenerateLeadDataExcel.as_view()),
    url(r'^(?P<form_id>[A-Z_a-z0-9]+)/delete_form$', DeleteLeadForm.as_view()),
    url(r'^(?P<form_id>[A-Z_a-z0-9]+)/delete_entry/(?P<entry_id>[A-Z_a-z0-9]+)$', DeleteLeadEntry.as_view()),
    url(r'^sanitize_leads_data/$', SanitizeLeadsData.as_view()),
    url(r'^(?P<form_id>[0-9]+)/add_sms_contact$', SmsContact.as_view()),
    url(r'^(?P<form_id>[0-9]+)/get_sms_contacts$', SmsContact.as_view()),
    url(r'^(?P<form_id>[0-9]+)/edit_leads_data', EditLeadsData.as_view()),
    url(r'^(?P<form_id>[0-9]+)/add_fields', AddLeadFormItems.as_view()),
    url(r'^(?P<form_id>[0-9]+)/edit_form_name', EditLeadsForm.as_view()),
    url(r'^summary/', LeadsSummary.as_view()),
    url(r'^migrate_leads_to_mongo/$', MigrateLeadsToMongo.as_view()),
    url(r'^generate_demo_data/$', GenerateDemoData.as_view()),
    url(r'^update_leads_data_sha256/$', UpdateLeadsDataSHA256.as_view()),
    url(r'^update_global_hot_lead_criteria/$', UpdateGlobalHotLeadCriteria.as_view()),
    url(r'^update_all_is_hot/$', UpdateLeadsDataIsHot.as_view()),

]

router = DefaultRouter()
router.include_format_suffixes = False
urlpatterns += router.urls
