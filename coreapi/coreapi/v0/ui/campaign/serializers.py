from rest_framework.serializers import ModelSerializer
from models import Campaign, CampaignSupplierTypes, CampaignTypeMapping, CampaignSocietyMapping


class CampaignSerializer(ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignSupplierTypesSerializer(ModelSerializer):
    class Meta:
        model = CampaignSupplierTypes
        fields = '__all__'


class CampaignTypeMappingSerializer(ModelSerializer):
    class Meta:
        model = CampaignTypeMapping
        fields = '__all__'


class CampaignSocietyMappingSerializer(ModelSerializer):
    class Meta:
        model = CampaignSocietyMapping
        fields = '__all__'
        depth = 1