from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from v0.ui.website.views import CreateInitialProposalBulkBasic,HashtagImagesViewSet
from views import SupplierPhaseViewSet

urlpatterns = [
    url(r'^create-initial-proposal-basic/$', CreateInitialProposalBulkBasic.as_view())
]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^hashtag-images', HashtagImagesViewSet, base_name='hashtag-images')
router.register(r'^supplier-phase', SupplierPhaseViewSet, base_name='supplier-phase')


urlpatterns += router.urls
