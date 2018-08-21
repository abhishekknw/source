from django.conf.urls import url
from views import (CreateChecklistTemplate, ChecklistEntry, GetCampaignChecklists,
    GetSupplierChecklists, GetChecklistData, DeleteChecklist, DeleteChecklistItems, DeleteChecklistRow)

urlpatterns = [
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/create$', CreateChecklistTemplate.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/enter_data$', ChecklistEntry.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/list_campaign_checklists$', GetCampaignChecklists.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/list_supplier_checklists/(?P<supplier_id>[A-Z_a-z0-9]+)$', GetSupplierChecklists.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/get_data$', GetChecklistData.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/delete_checklist$', DeleteChecklist.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/delete_field/(?P<item_id>[A-Z_a-z0-9]+)$', DeleteChecklistItems.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/delete_entry/(?P<entry_id>[A-Z_a-z0-9]+)$', DeleteChecklistRow.as_view()),

]