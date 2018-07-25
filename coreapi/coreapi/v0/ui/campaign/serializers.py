from rest_framework.serializers import ModelSerializer
from models import Campaign, CampaignSupplierTypes, CampaignTypeMapping, CampaignSocietyMapping
from rest_framework import serializers

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

class CampaignListSerializer(ModelSerializer):
    types = CampaignTypeMappingSerializer(source='get_types', many=True)
    society_count = serializers.IntegerField(source='get_society_count')
    info = serializers.DictField(source='get_info')

    class Meta:
        model = Campaign
        depth=1
        fields = '__all__'
        read_only_fields = (
        'types',
        'society_count',
        'info'
        )
