from django.contrib.auth.models import User, Permission, Group

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import CampaignSupplierTypes, SocietyInventoryBooking, CampaignSocietyMapping, CampaignTypeMapping, \
    Campaign, BusinessInfo, BusinessAccountContact, BusinessTypes, BusinessSubTypes, ImageMapping, InventoryLocation, \
    AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, \
    CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, \
    SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, \
    OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, FlyerInventory, \
    StreetFurniture, SportsInfra, SupplierInfo, SupplierTypeSociety, SupplierTypeCorporate, SocietyTower, FlatType, \
    AccountInfo, ContactDetailsGeneric, SupplierTypeSalon, SupplierTypeGym
from v0.models import City, CityArea, CitySubArea, SupplierTypeCode, InventorySummary, SocietyMajorEvents, \
    UserProfile, CorporateParkCompanyList, CorporateBuilding, CorporateBuildingWing, CorporateCompanyDetails, \
    CompanyFloor
import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.BaseUser


class UserProfileSerializer(ModelSerializer):
    # user1 = UserSerializer(source='get_user')
    class Meta:
        model = UserProfile
        # read_only_fields = (
    #    'user1'
    # )


class ImageMappingSerializer(ModelSerializer):
    class Meta:
        model = ImageMapping


class InventoryLocationSerializer(ModelSerializer):
    class Meta:
        model = InventoryLocation


class AdInventoryLocationMappingSerializer(ModelSerializer):
    class Meta:
        model = AdInventoryLocationMapping


class AdInventoryTypeSerializer(ModelSerializer):
    class Meta:
        model = AdInventoryType
        exclude = ('created_at', 'updated_at')


class DurationTypeSerializer(ModelSerializer):
    class Meta:
        model = DurationType
        exclude = ('created_at', 'updated_at')


class PriceMappingSerializer(ModelSerializer):
    class Meta:
        model = PriceMapping
        depth = 2


class BannerInventorySerializer(ModelSerializer):
    class Meta:
        model = BannerInventory


'''class CarDisplayInventorySerializer(ModelSerializer):

	class Meta:
		model = CarDisplayInventory'''


class CommunityHallInfoSerializer(ModelSerializer):
    class Meta:
        model = CommunityHallInfo


class DoorToDoorInfoSerializer(ModelSerializer):
    class Meta:
        model = DoorToDoorInfo


class LiftDetailsSerializer(ModelSerializer):
    tower_name = serializers.CharField(source='get_tower_name')

    class Meta:
        model = LiftDetails
        read_only_fields = (
            'tower_name'
        )


class NoticeBoardDetailsSerializer(ModelSerializer):
    tower_name = serializers.CharField(source='get_tower_name')

    class Meta:
        model = NoticeBoardDetails
        read_only_fields = (
            'tower_name'
        )


class PosterInventorySerializer(ModelSerializer):
    class Meta:
        model = PosterInventory


class SocietyFlatSerializer(ModelSerializer):
    class Meta:
        model = SocietyFlat


class StandeeInventorySerializer(ModelSerializer):
    class Meta:
        model = StandeeInventory


class SwimmingPoolInfoSerializer(ModelSerializer):
    class Meta:
        model = SwimmingPoolInfo


class WallInventorySerializer(ModelSerializer):
    class Meta:
        model = WallInventory


class UserInquirySerializer(ModelSerializer):
    class Meta:
        model = UserInquiry


class CommonAreaDetailsSerializer(ModelSerializer):
    class Meta:
        model = CommonAreaDetails


class ContactDetailsSerializer(ModelSerializer):
    class Meta:
        model = ContactDetails


class ContactDetailsGenericSerializer(ModelSerializer):
    class Meta:
        model = ContactDetailsGeneric
        depth = 2


class EventsSerializer(ModelSerializer):
    class Meta:
        model = Events


class InventoryInfoSerializer(ModelSerializer):
    class Meta:
        model = InventoryInfo


class MailboxInfoSerializer(ModelSerializer):
    class Meta:
        model = MailboxInfo


class OperationsInfoSerializer(ModelSerializer):
    class Meta:
        model = OperationsInfo


class PoleInventorySerializer(ModelSerializer):
    class Meta:
        model = PoleInventory


class PosterInventoryMappingSerializer(ModelSerializer):
    class Meta:
        model = PosterInventoryMapping


class RatioDetailsSerializer(ModelSerializer):
    class Meta:
        model = RatioDetails


class SignupSerializer(ModelSerializer):
    class Meta:
        model = Signup


class StallInventorySerializer(ModelSerializer):
    class Meta:
        model = StallInventory


class FlyerInventorySerializer(ModelSerializer):
    class Meta:
        model = FlyerInventory


class StreetFurnitureSerializer(ModelSerializer):
    class Meta:
        model = StreetFurniture


class SupplierInfoSerializer(ModelSerializer):
    class Meta:
        model = SupplierInfo


class SportsInfraSerializer(ModelSerializer):
    class Meta:
        model = SportsInfra


class SupplierTypeSocietySerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSociety
        fields = ('supplier_id', 'society_name', 'society_address1', 'society_address2', 'society_zip', 'society_city',
                  'society_state', 'society_longitude', 'society_locality', 'society_subarea', 'society_latitude', 'society_location_type',
                  'society_type_quality', 'society_type_quantity', 'flat_count', 'flat_avg_rental_persqft', 'flat_sale_cost_persqft',
                  'tower_count', 'payment_details_available', 'age_of_society','total_tenant_flat_count',
                  )



class SupplierTypeCorporateSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCorporate


class SupplierTypeSalonSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSalon


class SupplierTypeGymSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeGym


class CorporateParkCompanyListSerializer(ModelSerializer):
    class Meta:
        model = CorporateParkCompanyList


class SocietyTowerSerializer(ModelSerializer):
    class Meta:
        model = SocietyTower


class FlatTypeSerializer(ModelSerializer):
    class Meta:
        model = FlatType


class InventorySummarySerializer(ModelSerializer):
    class Meta:
        model = InventorySummary


class PriceMappingDefaultSerializer(ModelSerializer):
    class Meta:
        model = PriceMappingDefault
        depth = 1


class CampaignSupplierTypesSerializer(ModelSerializer):
    class Meta:
        model = CampaignSupplierTypes


class CampaignTypeMappingSerializer(ModelSerializer):
    class Meta:
        model = CampaignTypeMapping


class SocietyInventoryBookingSerializer(ModelSerializer):
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:
        model = SocietyInventoryBooking
        read_only_fields = (
            'type'
        )


class CampaignSerializer(ModelSerializer):
    class Meta:
        model = Campaign


class CampaignSocietyMappingSerializer(ModelSerializer):
    class Meta:
        model = CampaignSocietyMapping
        depth = 1


class BusinessSubTypesSerializer(ModelSerializer):
    class Meta:
        model = BusinessSubTypes


class BusinessTypesSerializer(ModelSerializer):
    class Meta:
        model = BusinessTypes

#
# class BusinessInfoSerializer(ModelSerializer):
#     # sub_type = BusinessSubTypesSerializer()
#     # type = BusinessTypesSerializer()
#     class Meta:
#         model = BusinessInfo
#         depth = 2

        # fields = ('id','name','type','sub_type','phone','email','address','reference_name',
        # 'reference_phone', 'reference_email', 'comments')


class BusinessAccountContactSerializer(ModelSerializer):
    class Meta:
        model = BusinessAccountContact

#
# class BusinessTypesSerializer(ModelSerializer):
#     class Meta:
#         model = BusinessTypes
#


class BusinessInfoSerializer(ModelSerializer):
    # sub_type = BusinessSubTypesSerializer()
    # type = BusinessTypesSerializer()
    class Meta:
        model = BusinessInfo
        # fields = ('id','name','type','sub_type','phone','email','address','reference_name',
        # 'reference_phone', 'reference_email', 'comments')


# class BusinessAccountContactSerializer(ModelSerializer):
#     class Meta:
#         model = BusinessAccountContact


class AccountInfoSerializer(ModelSerializer):
    class Meta:
        model = AccountInfo
        # depth = 1


class AccountSerializer(ModelSerializer):
    class Meta:
        model = AccountInfo

# class AccountContactSerializer(ModelSerializer):

#     class Meta:
#         model = AccountContact


class CitySubAreaSerializer(ModelSerializer):
    class Meta:
        model = CitySubArea


class CityAreaSerializer(ModelSerializer):
    class Meta:
        model = CityArea


class CitySerializer(ModelSerializer):
    class Meta:
        model = City


class SupplierTypeCodeSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCode


class SocietyMajorEventsSerializer(ModelSerializer):
    class Meta:
        model = SocietyMajorEvents


# CorporateBuilding, CorporateBuildingWing, CorporateCompany, CorporateCompanyDetails, CompanyFloor


class CorporateBuildingSerializer(ModelSerializer):
    class Meta:
        model = CorporateBuilding


class CorporateBuildingWingSerializer(ModelSerializer):
    class Meta:
        model = CorporateBuildingWing


class CorporateBuildingGetSerializer(ModelSerializer):
    wingInfo = CorporateBuildingWingSerializer(source='get_wings', many=True)

    class Meta:
        model = CorporateBuilding


class CompanyFloorSerializer(ModelSerializer):
    class Meta:
        model = CompanyFloor


class CorporateCompanySerializer(ModelSerializer):
    # for saving details of comapny with their building wing and floors /corporate/{{corporate_id}}/companyInfo
    listOfFloors = CompanyFloorSerializer(source='get_floors', many=True)

    class Meta:
        model = CorporateCompanyDetails


class CorporateParkCompanySerializer(ModelSerializer):
    # for saving details of comapny with their building wing and floors /corporate/{{corporate_id}}/companyInfo
    companyDetailList = CorporateCompanySerializer(source='get_company_details', many=True)

    class Meta:
        model = CorporateParkCompanyList


class CorporateCompanyDetailsSerializer(ModelSerializer):
    class Meta:
        model = CorporateCompanyDetails


class SupplierTypeBusShelterSerializer(ModelSerializer):
    class Meta:
        model = models.SupplierTypeBusShelter


class ProposalMasterCostSerializer(ModelSerializer):
    class Meta:
        model = models.ProposalMasterCost


class PrintingCostSerializer(ModelSerializer):
    class Meta:
        model = models.PrintingCost


class LogisticOperationsCostSerializer(ModelSerializer):
    class Meta:
        model = models.LogisticOperationsCost


class IdeationDesignCostSerializer(ModelSerializer):
    class Meta:
        model = models.IdeationDesignCost


class SpaceBookingCostSerializer(ModelSerializer):
    class Meta:
        model = models.SpaceBookingCost


class EventStaffingCostSerializer(ModelSerializer):
    class Meta:
        model = models.EventStaffingCost


class DataSciencesCostSerializer(ModelSerializer):
    class Meta:
        model = models.DataSciencesCost


class ProposalMetricsSerializer(ModelSerializer):
    class Meta:
        model = models.ProposalMetrics


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission


class BusinessTypeSubTypeReadOnlySerializer(ModelSerializer):
    subtypes = BusinessSubTypesSerializer(source='business_subtypes', many=True)

    class Meta:
        model = BusinessTypes

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group


class PermissionsSerializer(ModelSerializer):
    class Meta:
        model = Permission


class BaseUserSerializer(ModelSerializer):
    """
    You can only write a password. Not allowed to read it. Hence password is in extra_kwargs dict.
    when creating a BaseUser instance we want password to be saved by .set_password() method, hence overwritten to
    do that.
    When updating the BaseUser, we never update the password. There is a separate api for updating password.
    """
    groups = GroupSerializer(read_only=True,  many=True)
    user_permissions = PermissionsSerializer(read_only=True,  many=True)

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
        # hit save
        user.save()
        # return
        return user

    
    class Meta:
        model = models.BaseUser
        fields = ('id', 'first_name', 'last_name', 'email', 'user_code', 'username', 'mobile', 'password', 'is_superuser', 'groups', 'user_permissions')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class BaseUserUpdateSerializer(ModelSerializer):
    """

    """
    def update(self, instance, validated_data):
        """
        Args:
            instance: The instance to be updated
            validated_data: a dict having data to be updated
        Returns: an updated instance
        """
        # if password provided, then update the password
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            del validated_data['password']
      
        for key, value in validated_data.iteritems():
            setattr(instance, key, value)

        instance.save()
        # return the updated instance
        return instance

    class Meta:
        model = models.BaseUser
        fields = ('id', 'first_name', 'last_name', 'email', 'user_code', 'username', 'mobile','is_superuser', 'groups', 'user_permissions')
       

class SupplierTypeRetailShopSerializer(ModelSerializer):

    class Meta:
        model = models.SupplierTypeRetailShop
