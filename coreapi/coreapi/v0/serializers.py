from rest_framework.serializers import ModelSerializer
from v0.models import MasterBannerInventory, MasterCarDisplayInventory, MasterCommunityHallInfo, MasterDoorToDoorInfo, MasterLiftDetails, MasterNoticeBoardDetails, MasterPosterInventory, MasterSocietyFlat, MasterStandeeInventory, MasterSwimmingPoolInfo, MasterWallInventory, UserInquiry, CommonAreaDetails, MasterContactDetails, MasterEvents, MasterInventoryInfo, MasterMailboxInfo, MasterOperationsInfo, MasterPoleInventory, MasterPosterInventoryMapping, MasterRatioDetails, MasterSignup, MasterStallInventory, MasterStreetFurniture, MasterSupplierInfo, MasterSupplierTypeSociety, MasterSupplierTypeSocietyTower


class MasterBannerInventorySerializer(ModelSerializer):

    class Meta:
        model = MasterBannerInventory


class MasterCarDisplayInventorySerializer(ModelSerializer):

    class Meta:
        model = MasterCarDisplayInventory


class MasterCommunityHallInfoSerializer(ModelSerializer):

    class Meta:
        model = MasterCommunityHallInfo


class MasterDoorToDoorInfoSerializer(ModelSerializer):

    class Meta:
        model = MasterDoorToDoorInfo


class MasterLiftDetailsSerializer(ModelSerializer):

    class Meta:
        model = MasterLiftDetails


class MasterNoticeBoardDetailsSerializer(ModelSerializer):

    class Meta:
        model = MasterNoticeBoardDetails


class MasterPosterInventorySerializer(ModelSerializer):

    class Meta:
        model = MasterPosterInventory


class MasterSocietyFlatSerializer(ModelSerializer):

    class Meta:
        model = MasterSocietyFlat


class MasterStandeeInventorySerializer(ModelSerializer):

    class Meta:
        model = MasterStandeeInventory


class MasterSwimmingPoolInfoSerializer(ModelSerializer):

    class Meta:
        model = MasterSwimmingPoolInfo


class MasterWallInventorySerializer(ModelSerializer):

    class Meta:
        model = MasterWallInventory


class UserInquirySerializer(ModelSerializer):

    class Meta:
        model = UserInquiry


class CommonAreaDetailsSerializer(ModelSerializer):

    class Meta:
        model = CommonAreaDetails


class MasterContactDetailsSerializer(ModelSerializer):

    class Meta:
        model = MasterContactDetails


class MasterEventsSerializer(ModelSerializer):

    class Meta:
        model = MasterEvents


class MasterInventoryInfoSerializer(ModelSerializer):

    class Meta:
        model = MasterInventoryInfo


class MasterMailboxInfoSerializer(ModelSerializer):

    class Meta:
        model = MasterMailboxInfo


class MasterOperationsInfoSerializer(ModelSerializer):

    class Meta:
        model = MasterOperationsInfo


class MasterPoleInventorySerializer(ModelSerializer):

    class Meta:
        model = MasterPoleInventory


class MasterPosterInventoryMappingSerializer(ModelSerializer):

    class Meta:
        model = MasterPosterInventoryMapping


class MasterRatioDetailsSerializer(ModelSerializer):

    class Meta:
        model = MasterRatioDetails


class MasterSignupSerializer(ModelSerializer):

    class Meta:
        model = MasterSignup


class MasterStallInventorySerializer(ModelSerializer):

    class Meta:
        model = MasterStallInventory


class MasterStreetFurnitureSerializer(ModelSerializer):

    class Meta:
        model = MasterStreetFurniture


class MasterSupplierInfoSerializer(ModelSerializer):

    class Meta:
        model = MasterSupplierInfo


class MasterSupplierTypeSocietySerializer(ModelSerializer):

    class Meta:
        model = MasterSupplierTypeSociety


class MasterSupplierTypeSocietyTowerSerializer(ModelSerializer):

    class Meta:
        model = MasterSupplierTypeSocietyTower
