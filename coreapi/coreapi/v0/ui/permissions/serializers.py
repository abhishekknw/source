from rest_framework.serializers import ModelSerializer
from v0.ui.permissions.models import ObjectLevelPermission, GeneralUserPermission, Role, RoleHierarchy, Filters
from django.contrib.auth.models import User, Permission, Group
from v0.ui.user.models import UserInquiry

class FiltersSerializer(ModelSerializer):
    class Meta:
        model = Filters
        fields = '__all__'


class UserInquirySerializer(ModelSerializer):
    class Meta:
        model = UserInquiry
        fields = '__all__'

class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class PermissionsSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class ObjectLevelPermissionSerializer(ModelSerializer):
    """
    serializer for Object Level Permissions
    """
    class Meta:
        model = ObjectLevelPermission
        fields = '__all__'

class GeneralUserPermissionSerializer(ModelSerializer):
    """
    serializer for GeneralUserPermissions
    """
    class Meta:
        model = GeneralUserPermission
        fields = '__all__'

class ObjectLevelPermissionViewSet(ModelSerializer):
    """

    """
    class Meta:
        model = ObjectLevelPermission
        fields = '__all__'


class RoleSerializer(ModelSerializer):
    """
    simple serializer for Role
    """
    class Meta:
        model = Role
        fields = '__all__'

class RoleHierarchySerializer(ModelSerializer):
    """
    simple serializer for RoleHierarchy
    """
    class Meta:
        model = RoleHierarchy
        fields = '__all__'