from django.conf.urls import include, url

urlpatterns = [
    url(r'^surveys/', include('v0.ui.surveys.urls')),
]
