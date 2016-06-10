from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from v0.models import CampaignSupplierTypes, SocietyInventoryBooking, CampaignSocietyMapping, CampaignTypeMapping, Campaign, Business, BusinessContact, ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SportsInfra, SupplierInfo, SupplierTypeSociety, SocietyTower, FlatType
from v0.models import City, CityArea, CitySubArea, SupplierTypeCode, InventorySummary, SocietyMajorEvents, JMN_society, UserProfile
from v0.models import Account, AccountContact, BusinessTypes, BusinessSubTypes
from django.contrib.auth.models import User




class UserSerializer(ModelSerializer):
    class Meta:
        model = User


class UserProfileSerializer(ModelSerializer):
    user1 = UserSerializer(source='get_user')
    class Meta:
        model = UserProfile
        read_only_fields = (
            'user1'
        )


class JMN_societySerializer(ModelSerializer):

    class Meta:
        model = JMN_society


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


class DurationTypeSerializer(ModelSerializer):

    class Meta:
        model = DurationType


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
        depth=1


class BusinessSubTypesSerializer(ModelSerializer):

    class Meta:
        model = BusinessSubTypes
        depth = 2


class BusinessTypesSerializer(ModelSerializer):

    class Meta:
        model = BusinessTypes


class BusinessSerializer(ModelSerializer):
    # sub_type = BusinessSubTypesSerializer()
    # type = BusinessTypesSerializer()
    class Meta:

        model = Business
        depth = 2
       
        # fields = ('id','name','type','sub_type','phone','email','address','reference_name',
            # 'reference_phone', 'reference_email', 'comments')



class BusinessContactSerializer(ModelSerializer):

    class Meta:
        model = BusinessContact


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account


class AccountContactSerializer(ModelSerializer):

    class Meta:
        model = AccountContact

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
