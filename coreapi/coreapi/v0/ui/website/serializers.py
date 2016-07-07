from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import BusinessInfo, BusinessAccountContact, Campaign, CampaignTypeMapping, CampaignSocietyMapping, SocietyInventoryBooking, AccountInfo
from v0.ui.serializers import UISocietySerializer
from v0.serializers import SocietyInventoryBookingSerializer, BusinessInfoSerializer, BusinessTypesSerializer, BusinessAccountContactSerializer, CampaignSerializer, CampaignTypeMappingSerializer, AdInventoryTypeSerializer, AccountInfoSerializer


from v0.models import SupplierTypeCorporate, ProposalInfo, ProposalCenterMapping, SpaceMapping, InventoryType, ShortlistedSpaces, SupplierTypeSociety

class ProposalInfoSerializer(ModelSerializer):

    class Meta:
        model = ProposalInfo


class InventoryTypeSerializer(ModelSerializer):

    class Meta:
        model = InventoryType


class SpaceMappingSerializer(ModelSerializer):

    class Meta:
        model = SpaceMapping


class ProposalCenterMappingSpaceSerializer(ModelSerializer):
    space_mappings = SpaceMappingSerializer(source='get_space_mappings')

    class Meta:
        model = ProposalCenterMapping


class ProposalCenterMappingSerializer(ModelSerializer):

    class Meta:
        model = ProposalCenterMapping


class ShortlistedSpacesSerializer(ModelSerializer):

    class Meta:
        model = ShortlistedSpaces



class ProposalSocietySerializer(ModelSerializer):
    '''This serializer sends the latitude and longitude of societies on map view page.
    On clicking on map marker info of the society will be displayed'''

    # shortlisted is just for grid view to allow remove and shortlist functionality easliy
    shortlisted = serializers.SerializerMethodField('return_false')

    def return_false(self,foo):
        return True

    class Meta:
        model = SupplierTypeSociety
        fields = (
            'supplier_id',
            'society_name',
            'society_address1',
            'society_subarea',
            'society_location_type',
            'society_longitude',
            'society_latitude',
            'shortlisted',
        )


class ProposalCorporateSerializer(ModelSerializer):
    ''' This Serializer sends the latitude and longitude of corporates on map view page.
    On clicking on map marker info of the corporate will be retrived'''

    # shortlisted is just for grid view to allow remove and shortlist functionality easliy
    shortlisted = serializers.SerializerMethodField('return_false')

    def return_false(self,foo):
        return False

    class Meta:
        model = SupplierTypeCorporate
        fields = (
            'supplier_id',
            'name',
            'address1',
            'subarea',
            'location_type',
            'longitude',
            'latitude',
        )



class UISocietyInventorySerializer(ModelSerializer):
    inventory_price = serializers.IntegerField(source='get_price')
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:

        model = SocietyInventoryBooking
        read_only_fields = (
        'inventory_price',
        'type'
        )


class UIBusinessInfoSerializer(ModelSerializer):
    contacts = BusinessAccountContactSerializer(source='get_contacts', many=True)

    class Meta:
        model = BusinessInfo
        depth = 2
        read_only_fields = (
        'contacts'
        )


class UIAccountInfoSerializer(ModelSerializer):
    contacts = BusinessAccountContactSerializer(source='get_contacts', many=True)

    class Meta:
        model = AccountInfo
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
