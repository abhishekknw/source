from django.contrib.auth.models import User, Permission, Group

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import BusinessTypes, BusinessSubTypes, ImageMapping, DurationType, \
    UserInquiry, Events, \
    OperationsInfo, Signup
from v0.ui.organisation.serializers import OrganisationSerializer
from v0.models import SocietyMajorEvents, \
    CorporateParkCompanyList, CorporateBuildingWing, CorporateCompanyDetails, \
    CompanyFloor
import models
from v0.ui.finances.models import RatioDetails, PrintingCost, LogisticOperationsCost, IdeationDesignCost, \
    SpaceBookingCost, EventStaffingCost, DataSciencesCost, DoorToDoorInfo
from v0.ui.supplier.models import CorporateBuilding
from v0.ui.components.models import CommunityHallInfo, LiftDetails, NoticeBoardDetails, SwimmingPoolInfo, \
    SocietyFlat, FlatType, SocietyTower, SportsInfra, MailboxInfo, CommonAreaDetails


class ImageMappingSerializer(ModelSerializer):
    class Meta:
        model = ImageMapping
        fields = '__all__'


class DurationTypeSerializer(ModelSerializer):
    class Meta:
        model = DurationType
        exclude = ('created_at', 'updated_at')


'''class CarDisplayInventorySerializer(ModelSerializer):

	class Meta:
		model = CarDisplayInventory'''

class UserInquirySerializer(ModelSerializer):
    class Meta:
        model = UserInquiry
        fields = '__all__'

class EventsSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class OperationsInfoSerializer(ModelSerializer):
    class Meta:
        model = OperationsInfo
        fields = '__all__'

class SignupSerializer(ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'

class CorporateParkCompanyListSerializer(ModelSerializer):
    class Meta:
        model = CorporateParkCompanyList
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

class SocietyMajorEventsSerializer(ModelSerializer):
    class Meta:
        model = SocietyMajorEvents
        fields = '__all__'


# CorporateBuilding, CorporateBuildingWing, CorporateCompany, CorporateCompanyDetails, CompanyFloor


class CorporateBuildingSerializer(ModelSerializer):
    class Meta:
        model = CorporateBuilding
        fields = '__all__'


class CorporateBuildingWingSerializer(ModelSerializer):
    class Meta:
        model = CorporateBuildingWing
        fields = '__all__'


class CorporateBuildingGetSerializer(ModelSerializer):
    wingInfo = CorporateBuildingWingSerializer(source='get_wings', many=True)

    class Meta:
        model = CorporateBuilding
        fields = '__all__'


class CompanyFloorSerializer(ModelSerializer):
    class Meta:
        model = CompanyFloor
        fields = '__all__'


class CorporateCompanySerializer(ModelSerializer):
    # for saving details of comapny with their building wing and floors /corporate/{{corporate_id}}/companyInfo
    listOfFloors = CompanyFloorSerializer(source='get_floors', many=True)

    class Meta:
        model = CorporateCompanyDetails
        fields = '__all__'


class CorporateParkCompanySerializer(ModelSerializer):
    # for saving details of comapny with their building wing and floors /corporate/{{corporate_id}}/companyInfo
    companyDetailList = CorporateCompanySerializer(source='get_company_details', many=True)

    class Meta:
        model = CorporateParkCompanyList
        fields = '__all__'


class CorporateCompanyDetailsSerializer(ModelSerializer):
    class Meta:
        model = CorporateCompanyDetails
        fields = '__all__'



class SpaceBookingCostSerializer(ModelSerializer):
    class Meta:
        model = SpaceBookingCost
        fields = '__all__'

class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
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


class PermissionsSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GeneralUserPermissionSerializer(ModelSerializer):
    """
    serializer for GeneralUserPermissions
    """
    class Meta:
        model = models.GeneralUserPermission
        fields = '__all__'


class ObjectLevelPermissionSerializer(ModelSerializer):
    """
    serializer for Object Level Permissions
    """
    class Meta:
        model = models.ObjectLevelPermission
        fields = '__all__'


class ProfileNestedSerializer(ModelSerializer):
    """
    Nested serializer for Profile
    """
    organisation = OrganisationSerializer()
    object_level_permission = ObjectLevelPermissionSerializer(many=True, source='objectlevelpermission_set')
    general_user_permission = GeneralUserPermissionSerializer(many=True, source='generaluserpermission_set')

    class Meta:
        model = models.Profile
        fields = '__all__'


class BaseUserCreateSerializer(ModelSerializer):
    """
    specifically for creating  User objects. There was a need for creating this as standard serializer
    was also containing a nested serializer. It's not possible to write to a serializer if it's nested
    as of Django 1.8.
    """

    def create(self, validated_data):
        """
        Args:
            validated_data: the data that is used to be create the user.

        Returns: sets the password of the user when it's created.
        """

        # get the password
        password = validated_data['password']
        # delete it from the validated_data because we do not want to save it as raw password
        del validated_data['password']
        user = self.Meta.model.objects.create(**validated_data)
        # save password this way
        user.set_password(password)
        # save profile
        user.save()
        # return
        return user

    class Meta:
        model = models.BaseUser
        fields = (
        'id', 'first_name', 'last_name', 'email', 'user_code', 'username', 'mobile', 'password', 'is_superuser', 'profile')
        extra_kwargs = {
            'password': {'write_only': True}
        }