from django.conf.urls import url
from v0.ui.website.views import CreateInitialProposalBulk

urlpatterns = [
    url(r'^create-initial-proposal-excel/$', CreateInitialProposalBulk.as_view())
]