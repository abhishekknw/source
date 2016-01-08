from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import MasterBannerInventory, MasterCarDisplayInventory, MasterCommunityHallInfo, MasterDoorToDoorInfo, MasterLiftDetails, MasterNoticeBoardDetails, MasterPosterInventory, MasterSocietyFlat, MasterStandeeInventory, MasterSwimmingPoolInfo, MasterWallInventory, UserInquiry, CommonAreaDetails, MasterContactDetails, MasterEvents, MasterInventoryInfo, MasterMailboxInfo, MasterOperationsInfo, MasterPoleInventory, MasterPosterInventoryMapping, MasterRatioDetails, MasterSignup, MasterStallInventory, MasterStreetFurniture, MasterSupplierInfo, MasterSupplierTypeSociety, MasterSupplierTypeSocietyTower
from v0.serializers import MasterBannerInventorySerializer, MasterCarDisplayInventorySerializer, MasterCommunityHallInfoSerializer, MasterDoorToDoorInfoSerializer, MasterLiftDetailsSerializer, MasterNoticeBoardDetailsSerializer, MasterPosterInventorySerializer, MasterSocietyFlatSerializer, MasterStandeeInventorySerializer, MasterSwimmingPoolInfoSerializer, MasterWallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, MasterContactDetailsSerializer, MasterEventsSerializer, MasterInventoryInfoSerializer, MasterMailboxInfoSerializer, MasterOperationsInfoSerializer, MasterPoleInventorySerializer, MasterPosterInventoryMappingSerializer, MasterRatioDetailsSerializer, MasterSignupSerializer, MasterStallInventorySerializer, MasterStreetFurnitureSerializer, MasterSupplierInfoSerializer, MasterSupplierTypeSocietySerializer, MasterSupplierTypeSocietyTowerSerializer

class UISocietySerializer(ModelSerializer):
    basic_contact_available = serializers.BooleanField(source='is_contact_available')
    basic_contacts = MasterContactDetailsSerializer(source='get_contact_list', many=True)
    basic_reference_available = serializers.BooleanField(source='is_reference_available')
    #basic_reference_contacts = serializers.ListField(source='get_reference')
    class Meta:
        model = MasterSupplierTypeSociety
        read_only_fields = (
        'basic_contact_available',
        'basic_contacts',
        'basic_reference_available',
        'basic_reference_contacts',
        )


class UITowerSerializer(ModelSerializer):
    notice_board_details_available = serializers.BooleanField(source='is_notice_board_available')
    notice_board_details = MasterNoticeBoardDetailsSerializer(source='get_notice_board_list', many=True)
    flat_details_available = serializers.BooleanField(source='is_flat_available')
    flat_details = MasterSocietyFlatSerializer(source='get_flat_list', many=True)
    lift_details_available = serializers.BooleanField(source='is_lift_available')
    lift_details = MasterLiftDetailsSerializer(source='get_lift_list', many=True)
    #basic_reference_contacts = serializers.ListField(source='get_reference')
    class Meta:
        model = MasterSupplierTypeSocietyTower
        read_only_fields = (
        'notice_board_details_available',
        'flat_details_available',
        'lift_details_available',
        'flat_details',
        'notice_board_details',
        'lift_details',
        )


