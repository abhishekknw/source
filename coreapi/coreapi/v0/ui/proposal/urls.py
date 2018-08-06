from django.conf.urls import url
from v0.ui.website.views import CreateInitialProposalBulkBasic

urlpatterns = [
    url(r'^create-initial-proposal-basic/$', CreateInitialProposalBulkBasic.as_view())
]