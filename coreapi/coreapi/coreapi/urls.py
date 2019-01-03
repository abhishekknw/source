from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^api-token-', include('rest_jwt.urls')),
    url(r'^v0/', include('v0.urls')),
    url(r'^', include('v0.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

