from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import Business, BusinessContact, Campaign, CampaignTypeMapping, CampaignSocietyMapping
from v0.ui.serializers import UISocietySerializer
from v0.serializers import SocietyInventoryBookingSerializer, BusinessSerializer, BusinessContactSerializer, CampaignSerializer, CampaignTypeMappingSerializer

class UIBusinessSerializer(ModelSerializer):
    contact = BusinessContactSerializer(source='get_contact')

    class Meta:
        model = Business
        read_only_fields = (
        'contact'
        )


class CampaignListSerializer(ModelSerializer):
    types = CampaignTypeMappingSerializer(source='get_types', many=True)
    society_count = serializers.IntegerField(source='get_society_count')
    info = serializers.DictField(source='get_info')

    class Meta:
        model = Campaign
        depth=1
        read_only_fields = (
        'types',
        'society_count',
        'info'
        )

class CampaignInventorySerializer(ModelSerializer):
    inventories = SocietyInventoryBookingSerializer(source='get_inventories', many=True)
    campaign = CampaignSerializer(source='get_campaign')
    society = UISocietySerializer(source='get_society')

    class Meta:
        model = CampaignSocietyMapping
        read_only_fields = (
        'campaign',
        'society',
        'inventories'

        )