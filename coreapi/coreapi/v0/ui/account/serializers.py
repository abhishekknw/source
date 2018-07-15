from rest_framework.serializers import ModelSerializer
from models import BusinessAccountContact, AccountInfo, PriceMappingDefault, PriceMapping, ContactDetails, ContactDetailsGeneric
from v0.ui.organisation.models import Organisation
from v0.ui.base.serializers import BaseModelPermissionSerializer


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


class PriceMappingDefaultSerializer(ModelSerializer):
    class Meta:
        model = PriceMappingDefault
        fields = '__all__'
        depth = 1


class PriceMappingSerializer(ModelSerializer):
    class Meta:
        model = PriceMapping
        depth = 2
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