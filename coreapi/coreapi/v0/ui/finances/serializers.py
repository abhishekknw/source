from rest_framework.serializers import ModelSerializer
from models import DoorToDoorInfo, DataSciencesCost, EventStaffingCost, IdeationDesignCost, LogisticOperationsCost, \
    PriceMapping, PriceMappingDefault, PrintingCost, RatioDetails, SpaceBookingCost, SpaceBookingCost, \
    ShortlistedInventoryPricingDetails, AuditDate, ShortlistedInventoryComments
from v0.ui.inventory.serializers import InventoryActivitySerializerWithInventoryAssignmentsAndImages, \
    AdInventoryTypeSerializer, ShortlistedInventoryPricingSerializerReadOnly
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.base.serializers import DurationTypeSerializer
from v0.ui.user.serializers import BaseUserSerializer


class AuditDateSerializer(ModelSerializer):

    class Meta:
        model = AuditDate
        fields = '__all__'

class SpaceBookingCostSerializer(ModelSerializer):
    class Meta:
        model = SpaceBookingCost
        fields = '__all__'

class DataSciencesCostSerializer(ModelSerializer):
    class Meta:
        model = DataSciencesCost
        fields = '__all__'

class DoorToDoorInfoSerializer(ModelSerializer):
    class Meta:
        model = DoorToDoorInfo
        fields = '__all__'

class EventStaffingCostSerializer(ModelSerializer):
    class Meta:
        model = EventStaffingCost
        fields = '__all__'

class IdeationDesignCostSerializer(ModelSerializer):
    class Meta:
        model = IdeationDesignCost
        fields = '__all__'

class LogisticOperationsCostSerializer(ModelSerializer):
    class Meta:
        model = LogisticOperationsCost
        fields = '__all__'

class PriceMappingDefaultSerializer(ModelSerializer):
    class Meta:
        model = PriceMappingDefault
        fields = '__all__'
        depth = 1


class PriceMappingSerializer(ModelSerializer):
    class Meta:
        model = PriceMapping
        depth = 2
        fields = '__all__'


class PrintingCostSerializer(ModelSerializer):
    class Meta:
        model = PrintingCost
        fields = '__all__'

class RatioDetailsSerializer(ModelSerializer):
    class Meta:
        model = RatioDetails
        fields = '__all__'

class SpaceBookingCostSerializer(ModelSerializer):
    class Meta:
        model = SpaceBookingCost
        fields = '__all__'



class ShortlistedSpacesSerializerReadOnly(ModelSerializer):

    shortlisted_inventories = ShortlistedInventoryPricingSerializerReadOnly(many=True, source='shortlistedinventorypricingdetails_set')

    class Meta:
        model = ShortlistedSpaces
        exclude = ('created_at', 'updated_at', 'space_mapping')

class PriceMappingDefaultSerializerReadOnly(ModelSerializer):

    inventory_type = AdInventoryTypeSerializer(source='adinventory_type')
    inventory_duration = DurationTypeSerializer(source='duration_type')

    class Meta:
        model = PriceMappingDefault
        fields = '__all__'

