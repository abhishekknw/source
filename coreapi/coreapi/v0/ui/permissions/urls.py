from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from views import RoleViewSet, GeneralUserPermissionViewSet, RoleHierarchyViewSet, ObjectLevelPermissionViewSet
urlpatterns = [

]

router = DefaultRouter()
router.include_format_suffixes = False
router.register(r'^object-level-permission', ObjectLevelPermissionViewSet, base_name='object-level-permission')
router.register(r'^general-user-permission', GeneralUserPermissionViewSet, base_name='general-user-permission')
router.register(r'^role', RoleViewSet, base_name='role')
router.register(r'^role-hierarchy', RoleHierarchyViewSet, base_name='role-hierarchy')
urlpatterns += router.urls
