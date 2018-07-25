from rest_framework.serializers import ModelSerializer
from models import DoorToDoorInfo, DataSciencesCost, EventStaffingCost, IdeationDesignCost, LogisticOperationsCost, \
    PriceMapping, PriceMappingDefault, PrintingCost, RatioDetails, SpaceBookingCost, DurationType, SpaceBookingCost

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

class DurationTypeSerializer(ModelSerializer):
    class Meta:
        model = DurationType
        exclude = ('created_at', 'updated_at')