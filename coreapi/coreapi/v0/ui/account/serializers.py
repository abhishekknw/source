from rest_framework.serializers import ModelSerializer
from models import BusinessAccountContact, AccountInfo, ContactDetails, ContactDetailsGeneric, BusinessTypes,\
    BusinessSubTypes, OperationsInfo, ActivityLog
from v0.ui.organisation.models import Organisation
from v0.ui.base.serializers import BaseModelPermissionSerializer
from v0.ui.account.models import Signup, Profile
from v0.ui.permissions.serializers import ObjectLevelPermissionSerializer, GeneralUserPermissionSerializer
from v0.ui.organisation.serializers import OrganisationSerializer

class ProfileSimpleSerializer(ModelSerializer):
    """
    simple serializer for Profile
    """
    class Meta:
        model = Profile
        fields = '__all__'

class OperationsInfoSerializer(ModelSerializer):
    class Meta:
        model = OperationsInfo
        fields = '__all__'

class BusinessAccountContactSerializer(ModelSerializer):
    class Meta:
        model = BusinessAccountContact
        fields = '__all__'

class BusinessTypesSerializer(ModelSerializer):
    class Meta:
        model = BusinessTypes
        fields = '__all__'

class BusinessInfoSerializer(ModelSerializer):
    # sub_type = BusinessSubTypesSerializer()
    # type = BusinessTypesSerializer()
    class Meta:
        model = Organisation  # Why Organisation????
        fields = '__all__'
        # fields = ('id','name','type','sub_type','phone','email','address','reference_name',
        # 'reference_phone', 'reference_email', 'comments')


class AccountInfoSerializer(BaseModelPermissionSerializer):

    class Meta:
        model = AccountInfo
        fields = '__all__'


class AccountSerializer(ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = '__all__'

class ContactDetailsSerializer(ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = '__all__'


class ContactDetailsGenericSerializer(ModelSerializer):
    class Meta:
        model = ContactDetailsGeneric
        fields = '__all__'
        depth = 2

class SignupSerializer(ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'

class ProfileNestedSerializer(ModelSerializer):
    """
    Nested serializer for Profile
    """
    organisation = OrganisationSerializer()
    object_level_permission = ObjectLevelPermissionSerializer(many=True, source='objectlevelpermission_set')
    general_user_permission = GeneralUserPermissionSerializer(many=True, source='generaluserpermission_set')

    class Meta:
        model = Profile
        fields = '__all__'

class BusinessSubTypesSerializer(ModelSerializer):
    class Meta:
        model = BusinessSubTypes
        fields = '__all__'

class BusinessTypeSubTypeReadOnlySerializer(ModelSerializer):
    subtypes = BusinessSubTypesSerializer(source='business_subtypes', many=True)

    class Meta:
        model = BusinessTypes
        fields = '__all__'

class ProfileNestedSerializer(ModelSerializer):
    """
    Nested serializer for Profile
    """
    organisation = OrganisationSerializer()
    object_level_permission = ObjectLevelPermissionSerializer(many=True, source='objectlevelpermission_set')
    general_user_permission = GeneralUserPermissionSerializer(many=True, source='generaluserpermission_set')

    class Meta:
        model = Profile
        fields = '__all__'

class BusinessTypeSerializer(ModelSerializer):

    class Meta:
        model = BusinessTypes
        fields = '__all__'


class BusinessSubTypeSerializer(ModelSerializer):
    class Meta:
        model = BusinessSubTypes
        fields = '__all__'

class UIBusinessInfoSerializer(ModelSerializer):

    contacts = BusinessAccountContactSerializer(source='get_contacts', many=True)
    type_name = BusinessTypeSerializer()
    sub_type = BusinessSubTypeSerializer()

    class Meta:
        model = Organisation
        fields = '__all__'


class UIAccountInfoSerializer(ModelSerializer):
    contacts = BusinessAccountContactSerializer(source='get_contacts', many=True)

    class Meta:
        model = AccountInfo
        fields = '__all__'

        # depth = 2

class ActivityLogSerializer(ModelSerializer):

    class Meta:
        model = ActivityLog
        fields = '__all__'

