from rest_framework.serializers import ModelSerializer
from models import (SocietyInventoryBooking, InventoryLocation, AdInventoryLocationMapping, AdInventoryType,
                    BannerInventory, PosterInventory, InventorySummary, StreetFurniture, StallInventory, FlyerInventory,
                    StandeeInventory, WallInventory, InventoryInfo, PoleInventory, PosterInventoryMapping,
                    GatewayArchInventory, InventoryActivity, InventoryTypeVersion, InventoryActivityImage, InventoryType,
                    InventoryActivityAssignment)
from v0.ui.campaign.models import CampaignSocietyMapping
from v0.ui.campaign.serializers import CampaignTypeMappingSerializer, CampaignListSerializer
from rest_framework import serializers
from v0.ui.serializers import UISocietySerializer
from v0.ui.base.serializers import DurationTypeSerializer
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.proposal.models import ShortlistedSpaces

class AdInventoryTypeSerializer(ModelSerializer):
    class Meta:
        model = AdInventoryType
        exclude = ('created_at', 'updated_at')

class InventoryActivityImageSerializer(ModelSerializer):
    class Meta:
        model = InventoryActivityImage
        fields = '__all__'

class InventoryActivityAssignmentSerializerWithImages(ModelSerializer):

    images = InventoryActivityImageSerializer(many=True, source='inventoryactivityimage_set')

    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'

class InventoryActivitySerializerWithInventoryAssignmentsAndImages(ModelSerializer):

    inventory_activity_assignment = InventoryActivityAssignmentSerializerWithImages(many=True, source='inventoryactivityassignment_set')

    class Meta:
        model = InventoryActivity
        exclude = ('created_at', 'updated_at')

class UISocietyInventorySerializer(ModelSerializer):
    inventory_price = serializers.IntegerField(source='get_price')
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:

        model = SocietyInventoryBooking
        fields = '__all__'
        read_only_fields = (
        'inventory_price',
        'type'
        )

class CampaignInventorySerializer(ModelSerializer):
    inventories = UISocietyInventorySerializer(source='get_inventories', many=True)
    campaign = CampaignListSerializer(source='get_campaign')
    society = UISocietySerializer(source='get_society')

    class Meta:
        model = CampaignSocietyMapping
        fields = '__all__'
        read_only_fields = (
        'campaign',
        'society',
        'inventories'

        )

class InventoryTypeSerializer(ModelSerializer):

    class Meta:
        model = InventoryType
        fields = '__all__'

class InventoryActivitySerializer(ModelSerializer):
    """
    General serializer for inventory activity
    """

    class Meta:
        model = InventoryActivity
        fields = '__all__'

class InventoryTypeVersionSerializer(ModelSerializer):

    class Meta:
        model = InventoryTypeVersion
        fields = '__all__'

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

class ShortlistedSpacesSerializer(ModelSerializer):

    class Meta:
        model = ShortlistedSpaces
        exclude = ('space_mapping', 'buffer_status')

class InventoryActivityAssignmentSerializer(ModelSerializer):
    """
    General serializer for inv act assignment
    """
    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'

class ShortlistedInventoryPricingSerializerWithShortlistedSpacesReadOnly(ModelSerializer):
    """

    """
    inventory_type = AdInventoryTypeSerializer(source='ad_inventory_type')
    inventory_duration = DurationTypeSerializer(source='ad_inventory_duration')
    shortlisted_supplier = ShortlistedSpacesSerializer(source='shortlisted_spaces')

    class Meta:
        model = ShortlistedInventoryPricingDetails
        fields = '__all__'

class InventoryActivityAssignmentSerializerReadOnly(ModelSerializer):
    """
    Read only serializer for Inventory Activity Assignment Model
    """

    images = InventoryActivityImageSerializer(many=True, source='inventoryactivityimage_set')
    shortlisted_inventory_details = ShortlistedInventoryPricingSerializerWithShortlistedSpacesReadOnly()

    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'

class ShortlistedInventoryPricingSerializerReadOnly(ModelSerializer):

    inventory_activities = InventoryActivitySerializerWithInventoryAssignmentsAndImages(many=True, source='inventoryactivity_set')
    inventory_type = AdInventoryTypeSerializer(source='ad_inventory_type')
    inventory_duration = DurationTypeSerializer(source='ad_inventory_duration')

    class Meta:
        model = ShortlistedInventoryPricingDetails
        exclude = ('created_at', 'updated_at', 'ad_inventory_type', 'ad_inventory_duration')

class InventoryActivityAssignmentWithShortlistedSpaceReadOnly(ModelSerializer):
    inventory_details = ShortlistedInventoryPricingSerializerWithShortlistedSpacesReadOnly(
        source='shortlisted_inventory_details')

    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'

class InventoryActivityImageSerializerReadOnly(ModelSerializer):

    inventory_assignment_details = InventoryActivityAssignmentWithShortlistedSpaceReadOnly(source='inventory_activity_assignment')

    class Meta:
        model = InventoryActivityImage
        fields = '__all__'
