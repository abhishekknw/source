from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

import v0.models as models
from v0.ui.proposal.models import SpaceMapping, SpaceMappingVersion
from v0.ui.user.models import BaseUser
from v0.ui.finances.models import AuditDate, ShortlistedInventoryPricingDetails, PriceMappingDefault
from v0.ui.base.serializers import DurationTypeSerializer
from v0.ui.serializers import UISocietySerializer
from v0.ui.user.serializers import BaseUserSerializer
from v0.ui.account.models import AccountInfo, Profile, GenericExportFileName, BusinessTypes, BusinessSubTypes
from v0.ui.account.serializers import BusinessAccountContactSerializer
from v0.ui.campaign.models import Campaign, CampaignSocietyMapping, CampaignAssignment
from v0.ui.campaign.serializers import CampaignTypeMappingSerializer
from v0.ui.organisation.models import Organisation
from v0.ui.inventory.models import SocietyInventoryBooking, SupplierTypeSociety, InventoryActivityImage, \
    InventoryActivityAssignment, InventoryTypeVersion, InventoryType, InventoryActivity
from v0.ui.inventory.serializers import AdInventoryTypeSerializer
from v0.ui.proposal.models import ProposalCenterMapping, ProposalCenterMappingVersion, ShortlistedSpaces, \
    ShortlistedSpacesVersion
from v0.ui.proposal.serializers import ProposalInfoSerializer
from v0.ui.supplier.models import SupplierTypeCorporate, SupplierAmenitiesMap
from v0.ui.components.models import Amenity
from v0.ui.permissions.models import Filters, ObjectLevelPermission, GeneralUserPermission, Role, RoleHierarchy

from v0.ui.leads.models import Lead, LeadAlias, Leads
from v0.ui.leads.serializers import LeadSerializer

class SpaceMappingVersionSerializer(ModelSerializer):
    class Meta:
        model = SpaceMappingVersion
        fields = '__all__'

class ShortlistedSpacesVersionSerializer(ModelSerializer):

    class Meta:
        model = ShortlistedSpacesVersion
        fields = '__all__'


class ProposalCenterMappingVersionSpaceSerializer(ModelSerializer):
    # this serializer is used to send data to front end with space_mappings objects
    # Not using to save them
    space_mappings = SpaceMappingVersionSerializer(source='get_space_mappings_versions')

    class Meta:
        model = ProposalCenterMappingVersion
        fields = '__all__'


class GenericExportFileSerializerReadOnly(ModelSerializer):
    """
    This is nested serializer. it does not support Write operations as of now. Careful before using it.
    Currently it is being used to show File data plus proposal data
    """
    proposal = ProposalInfoSerializer()
    user = BaseUserSerializer()
    assignment_detail = serializers.ReadOnlyField(source='calculate_assignment_detail')

    class Meta:
        model = GenericExportFileName
        fields = '__all__'


class SpaceMappingSerializer(ModelSerializer):

    class Meta:
        model = SpaceMapping
        fields = '__all__'


class ProposalCenterMappingSpaceSerializer(ModelSerializer):
    # this serializer is used to send data to front end with space_mappings objects
    # Not using to save them
    space_mappings = SpaceMappingSerializer(source='get_space_mappings')

    class Meta:
        model = ProposalCenterMapping
        fields = '__all__'

class ProposalSocietySerializer(ModelSerializer):
    '''This serializer sends the latitude and longitude of societies on map view page.
    On clicking on map marker info of the society will be displayed'''

    # shortlisted is just for grid view to allow remove and shortlist functionality easliy
    shortlisted = serializers.SerializerMethodField('return_true')
    buffer_status = serializers.SerializerMethodField('return_false')

    def return_true(self,foo):
        return True

    def return_false(self, foo):
        return False

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
            'buffer_status',
        )


class ProposalCorporateSerializer(ModelSerializer):
    ''' This Serializer sends the latitude and longitude of corporates on map view page.
    On clicking on map marker info of the corporate will be retrived'''

    # shortlisted is just for grid view to allow remove and shortlist functionality easliy
    shortlisted = serializers.SerializerMethodField('return_true')
    buffer_status = serializers.SerializerMethodField('return_false')

    def return_true(self,foo):
        return True

    def return_false(self, foo):
        return False

    class Meta:
        model = SupplierTypeCorporate
        fields = (
            'supplier_id',
            'name',
            'address1',
            'subarea',
            'longitude',
            'latitude',
            'shortlisted',
            'buffer_status',
        )

class BusinessTypeSerializer(ModelSerializer):

    class Meta:
        model = BusinessTypes
        fields = '__all__'


class BusinessSubTypeSerializer(ModelSerializer):

    class Meta:
        model = BusinessSubTypes
        fields = '__all__'



class UIBusinessInfoSerializer(ModelSerializer):

    contacts = BusinessAccountContactSerializer(source='get_contacts', many=True)
    type_name = BusinessTypeSerializer()
    sub_type = BusinessSubTypeSerializer()

    class Meta:
        model = Organisation
        fields = '__all__'

        # depth = 2


class UIAccountInfoSerializer(ModelSerializer):
    contacts = BusinessAccountContactSerializer(source='get_contacts', many=True)

    class Meta:
        model = AccountInfo
        fields = '__all__'

        # depth = 2


class CampaignAssignmentSerializerReadOnly(ModelSerializer):

    assigned_by = BaseUserSerializer()
    assigned_to = BaseUserSerializer()
    campaign = ProposalInfoSerializer()

    class Meta:
        model = CampaignAssignment
        fields = '__all__'

class PriceMappingDefaultSerializerReadOnly(ModelSerializer):

    inventory_type = AdInventoryTypeSerializer(source='adinventory_type')
    inventory_duration = DurationTypeSerializer(source='duration_type')

    class Meta:
        model = PriceMappingDefault
        fields = '__all__'


class OrganisationSerializer(ModelSerializer):

    class Meta:
        model = models.Organisation
        fields = '__all__'


class ProfileSimpleSerializer(ModelSerializer):
    """
    simple serializer for Profile
    """
    class Meta:
        model = Profile
        fields = '__all__'



class ContentTypeSerializer(ModelSerializer):

    class Meta:
        model =  ContentType
        fields = '__all__'

class GenericExportFileSerializer(ModelSerializer):
    """
    simple serializer for generic export file name
    """

    class Meta:
        model = GenericExportFileName
        fields = '__all__'
