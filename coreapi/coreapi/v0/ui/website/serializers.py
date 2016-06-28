from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import Business, BusinessContact, Campaign, CampaignTypeMapping, CampaignSocietyMapping, SocietyInventoryBooking, Account, AccountContact
from v0.ui.serializers import UISocietySerializer
from v0.serializers import SocietyInventoryBookingSerializer, BusinessSerializer, BusinessTypesSerializer, BusinessContactSerializer, CampaignSerializer, CampaignTypeMappingSerializer, AdInventoryTypeSerializer, AccountSerializer, AccountContactSerializer


class UISocietyInventorySerializer(ModelSerializer):
    inventory_price = serializers.IntegerField(source='get_price')
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:

        model = SocietyInventoryBooking
        read_only_fields = (
        'inventory_price',
        'type'
        )


class UIBusinessSerializer(ModelSerializer):
    contacts = BusinessContactSerializer(source='get_contact', many=True)

    class Meta:
        model = Business
        depth = 2
        read_only_fields = (
        'contacts'
        )


class UIAccountSerializer(ModelSerializer):
    contacts = AccountContactSerializer(source='get_contact', many=True)

    class Meta:
        model = Account
        depth = 2
        read_only_fields = (
        'contacts'
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
    inventories = UISocietyInventorySerializer(source='get_inventories', many=True)
    campaign = CampaignListSerializer(source='get_campaign')
    society = UISocietySerializer(source='get_society')

    class Meta:
        model = CampaignSocietyMapping
        read_only_fields = (
        'campaign',
        'society',
        'inventories'

        )
