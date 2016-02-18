from django.conf.urls import include, url
from v0.android.audit import views

urlpatterns = [
    url(r'^assigned_audits/$', views.AssignedAuditAPIListView.as_view()),


]

