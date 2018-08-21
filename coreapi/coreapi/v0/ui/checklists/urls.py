from django.conf.urls import url
from views import Test, CreateChecklistTemplate, ChecklistEntry, GetCampaignChecklists, GetSupplierChecklists

urlpatterns = [
    url(r'^test/$', Test.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/create$', CreateChecklistTemplate.as_view()),
    url(r'^(?P<checklist_id>[A-Z_a-z0-9]+)/enter_data$', ChecklistEntry.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/list_campaign_checklists$', GetCampaignChecklists.as_view()),
    url(r'^(?P<campaign_id>[A-Z_a-z0-9]+)/list_supplier_checklists/(?P<supplier_id>[A-Z_a-z0-9]+)$', GetSupplierChecklists.as_view()),
]