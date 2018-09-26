from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import ImportProposalCostData, InventoryComment

urlpatterns = [
url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/import-proposal-cost-data/$', ImportProposalCostData.as_view(),
    name='import-metric-data'),
url(r'^(?P<proposal_id>[A-Z_a-z0-9-]+)/inventory_comment/$', InventoryComment.as_view(),
    name='import-metric-data'),

]

router = DefaultRouter()
router.include_format_suffixes = False



urlpatterns += router.urls
