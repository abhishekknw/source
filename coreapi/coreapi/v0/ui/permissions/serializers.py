from rest_framework.serializers import ModelSerializer
from v0.ui.permissions.models import UserInquiry, ObjectLevelPermission, GeneralUserPermission
from django.contrib.auth.models import User, Permission, Group

class UserInquirySerializer(ModelSerializer):
    class Meta:
        model = UserInquiry
        fields = '__all__'

class PermissionSerializer(ModelSerializer):
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