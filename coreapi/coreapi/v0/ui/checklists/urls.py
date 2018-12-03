from django.conf.urls import url
from views import (CreateChecklistTemplate, ChecklistEntry, GetCampaignChecklists,
                   GetSupplierChecklists, GetChecklistData, DeleteChecklist,
                   DeleteChecklistRow, ChecklistEdit, FreezeChecklist, ChecklistPermissionsAPI, GetAllChecklists,
                   GetAllChecklistsTemplates)

urlpatterns = [
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/create$', CreateChecklistTemplate.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/enter_data$', ChecklistEntry.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/list_campaign_checklists$', GetCampaignChecklists.as_view()),
    url(r'^list_all_checklists/$', GetAllChecklists.as_view()),
    url(r'^list_all_checklists_templates/$', GetAllChecklistsTemplates.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/list_supplier_checklists/(?P<supplier_id>[A-Z_a-z0-9]+)$', GetSupplierChecklists.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/get_data$', GetChecklistData.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/delete_checklist$', DeleteChecklist.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/delete_row/(?P<row_id>[A-Z_a-z0-9]+)$', DeleteChecklistRow.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/edit', ChecklistEdit.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/freeze/(?P<state>[0-1]+)$', FreezeChecklist.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/freeze/(?P<state>[0-1]+)$', FreezeChecklist.as_view()),
    url(r'^permissions/$', ChecklistPermissionsAPI.as_view()),
]