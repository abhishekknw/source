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
