from rest_framework.serializers import ModelSerializer
from models import SocietyInventoryBooking
from v0.ui.campaign.serializers import CampaignTypeMappingSerializer


class SocietyInventoryBookingSerializer(ModelSerializer):
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:
        model = SocietyInventoryBooking
        fields = '__all__'
        read_only_fields = (
            'type'
        )
