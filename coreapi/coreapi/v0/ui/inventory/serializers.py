from rest_framework.serializers import ModelSerializer
from models import (SocietyInventoryBooking, InventoryLocation, AdInventoryLocationMapping, AdInventoryType,
                    BannerInventory, PosterInventory, InventorySummary, StreetFurniture, StallInventory, FlyerInventory,
                    StandeeInventory, WallInventory, InventoryInfo, PoleInventory, PosterInventoryMapping,
                    GatewayArchInventory)
from v0.ui.campaign.serializers import CampaignTypeMappingSerializer


class SocietyInventoryBookingSerializer(ModelSerializer):
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:
        model = SocietyInventoryBooking
        fields = '__all__'
        read_only_fields = (
            'type'
        )

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


class BannerInventorySerializer(ModelSerializer):
    class Meta:
        model = BannerInventory
        fields = '__all__'

class PosterInventorySerializer(ModelSerializer):
    class Meta:
        model = PosterInventory
        fields = '__all__'


class InventorySummarySerializer(ModelSerializer):
    class Meta:
        model = InventorySummary
        fields = '__all__'


class StreetFurnitureSerializer(ModelSerializer):
    class Meta:
        model = StreetFurniture
        fields = '__all__'


class StallInventorySerializer(ModelSerializer):
    class Meta:
        model = StallInventory
        fields = '__all__'


class FlyerInventorySerializer(ModelSerializer):
    class Meta:
        model = FlyerInventory
        fields = '__all__'


class StandeeInventorySerializer(ModelSerializer):
    class Meta:
        model = StandeeInventory
        fields = '__all__'


class WallInventorySerializer(ModelSerializer):
    class Meta:
        model = WallInventory
        fields = '__all__'


class InventoryInfoSerializer(ModelSerializer):
    class Meta:
        model = InventoryInfo
        fields = '__all__'


class PoleInventorySerializer(ModelSerializer):
    class Meta:
        model = PoleInventory
        fields = '__all__'


class PosterInventoryMappingSerializer(ModelSerializer):
    class Meta:
        model = PosterInventoryMapping
        fields = '__all__'


class GatewatArchInventorySerializer(ModelSerializer):
    class Meta:
        model = GatewayArchInventory
        fields = '__all__'
