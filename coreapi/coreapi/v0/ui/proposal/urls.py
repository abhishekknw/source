from django.conf.urls import url
from v0.ui.website.views import CreateInitialProposalBulk, CreateInitialProposalBulkBasic

urlpatterns = [
    url(r'^create-initial-proposal-excel/$', CreateInitialProposalBulk.as_view()),
    url(r'^create-initial-proposal-basic/$', CreateInitialProposalBulkBasic.as_view())
]