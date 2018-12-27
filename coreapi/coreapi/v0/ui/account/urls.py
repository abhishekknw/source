from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import (BusinessAPIListView, BusinessAccounts, Accounts, AccountAPIView, BusinessContacts, AccountContacts,
                   GetBusinessTypesAPIView, GetBusinessSubTypesAPIView, AccountViewSet, LoginLog, ProfileAPIView)

urlpatterns = [
    url(r'^businesses/$', BusinessAPIListView.as_view(), name='get-all-business-info'),
    url(r'^business/(?P<id>[A-Z_a-z0-9]+)$', BusinessAccounts.as_view(), name='get-one-business-data'),
    url(r'^accounts/$', Accounts.as_view()),
    url(r'^account/(?P<id>[A-Z_a-z0-9]+)$', AccountAPIView.as_view()),
    url(r'^newCampaign/$', BusinessContacts.as_view()),
    url(r'^newAccountCampaign/$', AccountContacts.as_view()),
    url(r'^create_business/load_business_types/$', GetBusinessTypesAPIView.as_view(), name='get-business-types'),
    url(r'^subtypes/(?P<id>[A-Z_a-z0-9]+)/$', GetBusinessSubTypesAPIView.as_view(), name='get-business-subtypes'),
    url(r'^get_login_log/$', LoginLog.as_view(), name='get-login-log'),
    url(r'^profiles/$', ProfileAPIView.as_view(), name='get-login-log'),
]

router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'^account', AccountViewSet, base_name='account')
urlpatterns += router.urls
