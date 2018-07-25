from rest_framework.serializers import ModelSerializer
from models import BusinessAccountContact, AccountInfo, ContactDetails, ContactDetailsGeneric
from v0.ui.organisation.models import Organisation
from v0.ui.base.serializers import BaseModelPermissionSerializer
from v0.ui.account.models import Signup, Profile
from v0.ui.permissions.serializers import ObjectLevelPermissionSerializer, GeneralUserPermissionSerializer
from v0.ui.organisation.serializers import OrganisationSerializer

class BusinessAccountContactSerializer(ModelSerializer):
    class Meta:
        model = BusinessAccountContact
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
