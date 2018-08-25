from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from v0.ui.website.views import CreateInitialProposalBulkBasic,HashtagImagesViewSet

urlpatterns = [
    url(r'^create-initial-proposal-basic/$', CreateInitialProposalBulkBasic.as_view())
]

router = DefaultRouter()
router.include_format_suffixes = False

router.register(r'^hashtag-images', HashtagImagesViewSet, base_name='hashtag-images')


urlpatterns += router.urls
