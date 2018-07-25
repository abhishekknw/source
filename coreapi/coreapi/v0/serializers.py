from django.contrib.auth.models import User, Permission, Group

from rest_framework.serializers import ModelSerializer

from v0.ui.account.models import BusinessTypes, BusinessSubTypes, OperationsInfo
from v0.ui.organisation.serializers import OrganisationSerializer
import models
from v0.ui.finances.models import RatioDetails, PrintingCost, LogisticOperationsCost, IdeationDesignCost, \
    SpaceBookingCost, EventStaffingCost, DataSciencesCost, DoorToDoorInfo, DurationType
from v0.ui.components.models import CommunityHallInfo, LiftDetails, NoticeBoardDetails, SwimmingPoolInfo, \
    SocietyFlat, FlatType, SocietyTower, SportsInfra, MailboxInfo, CommonAreaDetails, CorporateBuildingWing, \
    CompanyFloor
from v0.ui.supplier.serializers import CorporateCompanyDetails
from v0.ui.account.models import Profile

'''class CarDisplayInventorySerializer(ModelSerializer):

	class Meta:
		model = CarDisplayInventory'''

class OperationsInfoSerializer(ModelSerializer):
    class Meta:
        model = OperationsInfo
        fields = '__all__'

class BusinessSubTypesSerializer(ModelSerializer):
    class Meta:
        model = BusinessSubTypes
        fields = '__all__'


class BusinessTypesSerializer(ModelSerializer):
    class Meta:
        model = BusinessTypes
        fields = '__all__'

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

class CorporateCompanyDetailsSerializer(ModelSerializer):
    class Meta:
        model = CorporateCompanyDetails
        fields = '__all__'

class BusinessTypeSubTypeReadOnlySerializer(ModelSerializer):
    subtypes = BusinessSubTypesSerializer(source='business_subtypes', many=True)

    class Meta:
        model = BusinessTypes
        fields = '__all__'

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
