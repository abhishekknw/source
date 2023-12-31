from __future__ import absolute_import
from django.conf.urls import url
from .views import (CreateChecklistTemplate, ChecklistEntry, GetCampaignChecklists,
                   GetSupplierChecklists, GetChecklistData, DeleteChecklist,
                   DeleteChecklistRow, ChecklistEdit, FreezeChecklist, ChecklistPermissionsAPI, GetAllChecklists,
                   GetAllChecklistsTemplates, ChecklistPermissionsByProfileIdAPI, ChecklistSavedOperators,
                   ChecklistUnsavedOperators, ChecklistSavedOperatorsResult, ChecklistPermissionsSelfAPI)

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
    url(r'^permissions/self/$', ChecklistPermissionsSelfAPI.as_view()),
    url(r'^permissions/(?P<profile_id>[A-Z_a-z0-9]+)/$', ChecklistPermissionsByProfileIdAPI.as_view()),
    url(r'^metrics/$', ChecklistSavedOperators.as_view()),
    url(r'^unsaved-metrics/$', ChecklistUnsavedOperators.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/metrics/$', ChecklistSavedOperatorsResult.as_view()),
]