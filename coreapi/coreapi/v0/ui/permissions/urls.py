from django.conf.urls import url
from rest_framework.routers import DefaultRouter

urlpatterns = [

]

router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'^object-level-permission', views.ObjectLevelPermissionViewSet, base_name='object-level-permission')
router.register(r'^general-user-permission', views.GeneralUserPermissionViewSet, base_name='general-user-permission')
router.register(r'^role', views.RoleViewSet, base_name='role')
router.register(r'^role-hierarchy', views.RoleHierarchyViewSet, base_name='role-hierarchy')
urlpatterns += router.urls
