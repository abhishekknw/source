from django.conf.urls import url
from views import (GetLeadsDataGeneric)

urlpatterns = [
    url(r'^get-leads-data-generic/$', GetLeadsDataGeneric.as_view()),
]