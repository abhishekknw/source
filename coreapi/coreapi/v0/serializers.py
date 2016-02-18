from rest_framework.serializers import ModelSerializer
from v0.models import CampaignSocietyMapping, CampaignTypeMapping, Campaign, Business, BusinessContact, ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CarDisplayInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SportsInfra, SupplierInfo, SupplierTypeSociety, SocietyTower, FlatType



class CampaignTypeMappingSerializer(ModelSerializer):

    class Meta:
        model = CampaignTypeMapping


class CampaignSerializer(ModelSerializer):

    class Meta:
        model = Campaign


class CampaignSocietyMappingSerializer(ModelSerializer):

    class Meta:
        model = CampaignSocietyMapping
        depth=1



class BusinessSerializer(ModelSerializer):

    class Meta:
        model = Business


class BusinessContactSerializer(ModelSerializer):

    class Meta:
        model = BusinessContact

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



class PriceMappingDefaultSerializer(ModelSerializer):

    class Meta:
        model = PriceMappingDefault
        depth = 1

class PriceMappingSerializer(ModelSerializer):

    class Meta:
        model = PriceMapping
        depth = 2


class BannerInventorySerializer(ModelSerializer):

    class Meta:
        model = BannerInventory


class CarDisplayInventorySerializer(ModelSerializer):

    class Meta:
        model = CarDisplayInventory


class CommunityHallInfoSerializer(ModelSerializer):

    class Meta:
        model = CommunityHallInfo


class DoorToDoorInfoSerializer(ModelSerializer):

    class Meta:
        model = DoorToDoorInfo


class LiftDetailsSerializer(ModelSerializer):

    class Meta:
        model = LiftDetails


class NoticeBoardDetailsSerializer(ModelSerializer):

    class Meta:
        model = NoticeBoardDetails


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
