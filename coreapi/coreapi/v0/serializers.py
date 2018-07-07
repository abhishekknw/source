from django.contrib.auth.models import User, Permission, Group
from django.core.exceptions import PermissionDenied

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import CampaignSupplierTypes, SocietyInventoryBooking, CampaignSocietyMapping, CampaignTypeMapping, \
    Campaign, Organisation, BusinessAccountContact, BusinessTypes, BusinessSubTypes, ImageMapping, InventoryLocation, \
    AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, \
    CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, \
    SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, \
    OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, FlyerInventory, \
    StreetFurniture, SportsInfra, SupplierInfo, SupplierTypeSociety, SupplierTypeCorporate, SocietyTower, FlatType, \
    AccountInfo, ContactDetailsGeneric, SupplierTypeSalon, SupplierTypeGym
from v0.models import SupplierTypeCode, InventorySummary, SocietyMajorEvents, \
    CorporateParkCompanyList, CorporateBuilding, CorporateBuildingWing, CorporateCompanyDetails, \
    CompanyFloor
import models
import v0.constants as v0_constants
from managers import check_object_permission


class BaseModelPermissionSerializer(ModelSerializer):
      """

      Inherit this serializer if you want permission checking in creation of  a model instance through serializer.
      Not sure weather to do this in .save() method or here. Going with serializer.

      """
      def create(self, validated_data):
          """
          called in creating instance. Here we only check fo 'CREATE' permission for the given user.
          :param validated_data:
          :return:
          """
          class_name = self.__class__.__name__
          is_permission, error = check_object_permission(validated_data['user'], self.Meta.model, v0_constants.permission_contants['CREATE'])
          if not is_permission:
              raise PermissionDenied(class_name, error)
          return self.Meta.model.objects.create(**validated_data)


class AccountInfoSerializer(BaseModelPermissionSerializer):

    class Meta:
        model = AccountInfo
        fields = '__all__'


class ImageMappingSerializer(ModelSerializer):
    class Meta:
        model = ImageMapping
        fields = '__all__'


class InventoryLocationSerializer(ModelSerializer):
    class Meta:
        model = InventoryLocation
        fields = '__all__'


class AdInventoryLocationMappingSerializer(ModelSerializer):
    class Meta:
        model = AdInventoryLocationMapping
        fields = '__all__'


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
        fields = '__all__'


class BannerInventorySerializer(ModelSerializer):
    class Meta:
        model = BannerInventory
        fields = '__all__'


'''class CarDisplayInventorySerializer(ModelSerializer):

	class Meta:
		model = CarDisplayInventory'''


class CommunityHallInfoSerializer(ModelSerializer):
    class Meta:
        model = CommunityHallInfo
        fields = '__all__'


class DoorToDoorInfoSerializer(ModelSerializer):
    class Meta:
        model = DoorToDoorInfo
        fields = '__all__'


class LiftDetailsSerializer(ModelSerializer):
    tower_name = serializers.CharField(source='get_tower_name')

    class Meta:
        model = LiftDetails
        fields = '__all__'
        read_only_fields = (
            'tower_name'
        )


class NoticeBoardDetailsSerializer(ModelSerializer):
    tower_name = serializers.CharField(source='get_tower_name')

    class Meta:
        model = NoticeBoardDetails
        fields = '__all__'
        read_only_fields = (
            'tower_name'
        )


class PosterInventorySerializer(ModelSerializer):
    class Meta:
        model = PosterInventory
        fields = '__all__'


class SocietyFlatSerializer(ModelSerializer):
    class Meta:
        model = SocietyFlat
        fields = '__all__'


class StandeeInventorySerializer(ModelSerializer):
    class Meta:
        model = StandeeInventory
        fields = '__all__'


class SwimmingPoolInfoSerializer(ModelSerializer):
    class Meta:
        model = SwimmingPoolInfo
        fields = '__all__'


class WallInventorySerializer(ModelSerializer):
    class Meta:
        model = WallInventory
        fields = '__all__'


class UserInquirySerializer(ModelSerializer):
    class Meta:
        model = UserInquiry
        fields = '__all__'


class CommonAreaDetailsSerializer(ModelSerializer):
    class Meta:
        model = CommonAreaDetails
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


class EventsSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class InventoryInfoSerializer(ModelSerializer):
    class Meta:
        model = InventoryInfo
        fields = '__all__'


class MailboxInfoSerializer(ModelSerializer):
    class Meta:
        model = MailboxInfo
        fields = '__all__'


class OperationsInfoSerializer(ModelSerializer):
    class Meta:
        model = OperationsInfo
        fields = '__all__'


class PoleInventorySerializer(ModelSerializer):
    class Meta:
        model = PoleInventory
        fields = '__all__'


class PosterInventoryMappingSerializer(ModelSerializer):
    class Meta:
        model = PosterInventoryMapping
        fields = '__all__'


class RatioDetailsSerializer(ModelSerializer):
    class Meta:
        model = RatioDetails
        fields = '__all__'


class SignupSerializer(ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'


class StallInventorySerializer(ModelSerializer):
    class Meta:
        model = StallInventory
        fields = '__all__'


class FlyerInventorySerializer(ModelSerializer):
    class Meta:
        model = FlyerInventory
        fields = '__all__'


class StreetFurnitureSerializer(ModelSerializer):
    class Meta:
        model = StreetFurniture
        fields = '__all__'


class SupplierInfoSerializer(ModelSerializer):
    class Meta:
        model = SupplierInfo
        fields = '__all__'


class SportsInfraSerializer(ModelSerializer):
    class Meta:
        model = SportsInfra
        fields = '__all__'


class SupplierTypeSocietySerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSociety
        fields = ('supplier_id', 'society_name', 'society_address1', 'society_address2', 'society_zip', 'society_city',
                  'society_state', 'society_longitude', 'society_locality', 'society_subarea', 'society_latitude', 'society_location_type',
                  'society_type_quality', 'society_type_quantity', 'flat_count', 'flat_avg_rental_persqft', 'flat_sale_cost_persqft',
                  'tower_count', 'payment_details_available', 'age_of_society','total_tenant_flat_count','landmark','feedback',
                  )



class SupplierTypeCorporateSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCorporate
        fields = '__all__'


class SupplierTypeSalonSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeSalon
        fields = '__all__'


class SupplierTypeGymSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeGym
        fields = '__all__'


class CorporateParkCompanyListSerializer(ModelSerializer):
    class Meta:
        model = CorporateParkCompanyList
        fields = '__all__'


class SocietyTowerSerializer(ModelSerializer):
    class Meta:
        model = SocietyTower
        fields = '__all__'


class FlatTypeSerializer(ModelSerializer):
    class Meta:
        model = FlatType
        fields = '__all__'


class InventorySummarySerializer(ModelSerializer):
    class Meta:
        model = InventorySummary
        fields = '__all__'


class PriceMappingDefaultSerializer(ModelSerializer):
    class Meta:
        model = PriceMappingDefault
        fields = '__all__'
        depth = 1


class CampaignSupplierTypesSerializer(ModelSerializer):
    class Meta:
        model = CampaignSupplierTypes
        fields = '__all__'


class CampaignTypeMappingSerializer(ModelSerializer):
    class Meta:
        model = CampaignTypeMapping
        fields = '__all__'


class SocietyInventoryBookingSerializer(ModelSerializer):
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:
        model = SocietyInventoryBooking
        fields = '__all__'
        read_only_fields = (
            'type'
        )


class CampaignSerializer(ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignSocietyMappingSerializer(ModelSerializer):
    class Meta:
        model = CampaignSocietyMapping
        fields = '__all__'
        depth = 1


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


class BusinessAccountContactSerializer(ModelSerializer):
    class Meta:
        model = BusinessAccountContact
        fields = '__all__'

#
# class BusinessTypesSerializer(ModelSerializer):
#     class Meta:
#         model = BusinessTypes
#


class BusinessInfoSerializer(ModelSerializer):
    # sub_type = BusinessSubTypesSerializer()
    # type = BusinessTypesSerializer()
    class Meta:
        model = Organisation
        fields = '__all__'
        # fields = ('id','name','type','sub_type','phone','email','address','reference_name',
        # 'reference_phone', 'reference_email', 'comments')


# class BusinessAccountContactSerializer(ModelSerializer):
#     class Meta:
#         model = BusinessAccountContact



class AccountSerializer(ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = '__all__'

# class AccountContactSerializer(ModelSerializer):

#     class Meta:
#         model = AccountContact


class SupplierTypeCodeSerializer(ModelSerializer):
    class Meta:
        model = SupplierTypeCode
        fields = '__all__'


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


class SupplierTypeBusShelterSerializer(ModelSerializer):
    class Meta:
        model = models.SupplierTypeBusShelter
        fields = '__all__'


class ProposalMasterCostSerializer(ModelSerializer):
    class Meta:
        model = models.ProposalMasterCost
        fields = '__all__'


class PrintingCostSerializer(ModelSerializer):
    class Meta:
        model = models.PrintingCost
        fields = '__all__'


class LogisticOperationsCostSerializer(ModelSerializer):
    class Meta:
        model = models.LogisticOperationsCost
        fields = '__all__'


class IdeationDesignCostSerializer(ModelSerializer):
    class Meta:
        model = models.IdeationDesignCost
        fields = '__all__'


class SpaceBookingCostSerializer(ModelSerializer):
    class Meta:
        model = models.SpaceBookingCost
        fields = '__all__'


class EventStaffingCostSerializer(ModelSerializer):
    class Meta:
        model = models.EventStaffingCost
        fields = '__all__'


class DataSciencesCostSerializer(ModelSerializer):
    class Meta:
        model = models.DataSciencesCost
        fields = '__all__'


class ProposalMetricsSerializer(ModelSerializer):
    class Meta:
        model = models.ProposalMetrics
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


class OrganisationSerializer(BaseModelPermissionSerializer):

    class Meta:
        model = models.Organisation
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


class SupplierTypeRetailShopSerializer(ModelSerializer):

    class Meta:
        model = models.SupplierTypeRetailShop
        fields = '__all__'

class GatewatArchInventorySerializer(ModelSerializer):
    class Meta:
        model = models.GatewayArchInventory
        fields = '__all__'
