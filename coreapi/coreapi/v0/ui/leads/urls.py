from django.conf.urls import url
from views import LeadsViewSetExcel, CreateLeadsForm

urlpatterns = [
    url(r'^create-leads-excel/$', LeadsViewSetExcel.as_view()),
    url(r'^form/create$', CreateLeadsForm.as_view())
]