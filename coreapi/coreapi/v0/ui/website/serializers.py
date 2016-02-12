from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import Business, BusinessContact, Campaign, CampaignTypeMapping, CampaignSocietyMapping
from v0.ui.serializers import UISocietySerializer
from v0.serializers import BusinessSerializer, BusinessContactSerializer, CampaignSerializer, CampaignTypeMappingSerializer

class UIBusinessSerializer(ModelSerializer):
    contact = BusinessContactSerializer(source='get_contact')

    class Meta:
        model = Business
        read_only_fields = (
        'contact'
        )


class FinalizeCampaignSerializer(ModelSerializer):
    types = CampaignTypeMappingSerializer(source='get_types', many=True)

    class Meta:
        model = Campaign
        depth=1
        read_only_fields = (
        'types'
        )

class FinalizeInventorySerializer(ModelSerializer):
    campaign = FinalizeCampaignSerializer(source='get_campaign')
    society = UISocietySerializer(source='get_society')

    class Meta:
        model = CampaignSocietyMapping
        read_only_fields = (
        'campaign',
        'society'
        )