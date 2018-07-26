
from rest_framework.serializers import ModelSerializer

from v0.ui.account.models import BusinessTypes, BusinessSubTypes, OperationsInfo
from v0.ui.supplier.serializers import CorporateCompanyDetails
from v0.ui.account.models import Profile

#
# class BusinessInfoSerializer(ModelSerializer):
#     # sub_type = BusinessSubTypesSerializer()
#     # type = BusinessTypesSerializer()
#     class Meta:
#         model = Organisation
#         depth = 2

        # fields = ('id','name','type','sub_type','phone','email','address','reference_name',
        # 'reference_phone', 'reference_email', 'comments')


#
# class BusinessTypesSerializer(ModelSerializer):
#     class Meta:
#         model = BusinessTypes
#


# class BusinessAccountContactSerializer(ModelSerializer):
#     class Meta:
#         model = BusinessAccountContact


# class AccountContactSerializer(ModelSerializer):

#     class Meta:
#         model = AccountContact


# CorporateBuilding, CorporateBuildingWing, CorporateCompany, CorporateCompanyDetails, CompanyFloor