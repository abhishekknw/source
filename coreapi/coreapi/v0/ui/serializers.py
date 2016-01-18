from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import BannerInventory, CarDisplayInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SupplierTypeSociety, SocietyTower
from v0.serializers import BannerInventorySerializer, CarDisplayInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer

class UISocietySerializer(ModelSerializer):
    basic_contact_available = serializers.BooleanField(source='is_contact_available')
    basic_contacts = ContactDetailsSerializer(source='get_contact_list', many=True)
    basic_reference_available = serializers.BooleanField(source='is_reference_available')
    basic_reference_contacts = ContactDetailsSerializer(source='get_reference')

    past_details = serializers.BooleanField(source='is_past_details_available')
    business_preferences = serializers.BooleanField(source='is_business_preferences_available')
    class Meta:
        model = SupplierTypeSociety
        read_only_fields = (
        'basic_contact_available',
        'basic_contacts',
        'basic_reference_available',
        'basic_reference_contacts',
        'past_details',
        'business_preferences'
        )


class UITowerSerializer(ModelSerializer):
    notice_board_details_available = serializers.BooleanField(source='is_notice_board_available')
    notice_board_details = NoticeBoardDetailsSerializer(source='get_notice_board_list', many=True)
    flat_details_available = serializers.BooleanField(source='is_flat_available')
    flat_details = SocietyFlatSerializer(source='get_flat_list', many=True)
    lift_details_available = serializers.BooleanField(source='is_lift_available')
    lift_details = LiftDetailsSerializer(source='get_lift_list', many=True)
    #basic_reference_contacts = serializers.ListField(source='get_reference')
    class Meta:
        model = SocietyTower
        read_only_fields = (
        'notice_board_details_available',
        'flat_details_available',
        'lift_details_available',
        'flat_details',
        'notice_board_details',
        'lift_details',
        )




