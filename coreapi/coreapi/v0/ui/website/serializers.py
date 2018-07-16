from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

import v0.models as models
from v0.models import SpaceMapping, ShortlistedSpaces,\
                    SpaceMappingVersion, ShortlistedSpacesVersion, BaseUser
from v0.ui.finances.models import AuditDate, ShortlistedInventoryPricingDetails, PriceMappingDefault
from v0.ui.base.serializers import BaseModelPermissionSerializer
from v0.serializers import DurationTypeSerializer
from v0.ui.serializers import UISocietySerializer
from v0.ui.user.serializers import BaseUserSerializer
from v0.ui.account.models import AccountInfo
from v0.ui.account.serializers import BusinessAccountContactSerializer
from v0.ui.campaign.models import Campaign, CampaignSocietyMapping, CampaignAssignment
from v0.ui.campaign.serializers import CampaignTypeMappingSerializer
from v0.ui.organisation.models import Organisation
from v0.ui.inventory.models import SocietyInventoryBooking, SupplierTypeSociety, InventoryActivityImage, \
    InventoryActivityAssignment, InventoryTypeVersion, InventoryType, InventoryActivity
from v0.ui.inventory.serializers import AdInventoryTypeSerializer
from v0.ui.proposal.models import ProposalCenterMapping, ProposalCenterMappingVersion
from v0.ui.proposal.serializers import ProposalInfoSerializer
from v0.ui.supplier.models import SupplierTypeCorporate, SupplierAmenitiesMap

class InventoryActivitySerializer(ModelSerializer):
    """
    General serializer for inventory activity
    """

    class Meta:
        model = InventoryActivity
        fields = '__all__'


class LeadSerializer(ModelSerializer):
    class Meta:
        model = models.Lead
        fields = '__all__'


class FiltersSerializer(ModelSerializer):
    class Meta:
        model = models.Filters
        fields = '__all__'

class SpaceMappingVersionSerializer(ModelSerializer):
    class Meta:
        model = SpaceMappingVersion
        fields = '__all__'


class InventoryTypeVersionSerializer(ModelSerializer):

    class Meta:
        model = InventoryTypeVersion
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


class GuestUserSerializer(ModelSerializer):

    class Meta:
        model = BaseUser
        fields = ('id', 'first_name', 'last_name', 'email', 'user_code', 'username', 'mobile')


class GenericExportFileSerializerReadOnly(ModelSerializer):
    """
    This is nested serializer. it does not support Write operations as of now. Careful before using it.
    Currently it is being used to show File data plus proposal data
    """
    proposal = ProposalInfoSerializer()
    user = BaseUserSerializer()
    assignment_detail = serializers.ReadOnlyField(source='calculate_assignment_detail')

    class Meta:
        model = models.GenericExportFileName
        fields = '__all__'


class InventoryTypeSerializer(ModelSerializer):

    class Meta:
        model = InventoryType
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


class ShortlistedSpacesSerializer(ModelSerializer):

    class Meta:
        model = ShortlistedSpaces
        exclude = ('space_mapping', 'buffer_status')


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


class UISocietyInventorySerializer(ModelSerializer):
    inventory_price = serializers.IntegerField(source='get_price')
    type = CampaignTypeMappingSerializer(source='get_type')

    class Meta:

        model = SocietyInventoryBooking
        fields = '__all__'
        read_only_fields = (
        'inventory_price',
        'type'
        )



class BusinessTypeSerializer(ModelSerializer):

    class Meta:
        model = models.BusinessTypes
        fields = '__all__'


class BusinessSubTypeSerializer(ModelSerializer):

    class Meta:
        model = models.BusinessSubTypes
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

class CampaignInventorySerializer(ModelSerializer):
    inventories = UISocietyInventorySerializer(source='get_inventories', many=True)
    campaign = CampaignListSerializer(source='get_campaign')
    society = UISocietySerializer(source='get_society')

    class Meta:
        model = CampaignSocietyMapping
        fields = '__all__'
        read_only_fields = (
        'campaign',
        'society',
        'inventories'

        )


class CampaignAssignmentSerializerReadOnly(ModelSerializer):

    assigned_by = BaseUserSerializer()
    assigned_to = BaseUserSerializer()
    campaign = ProposalInfoSerializer()

    class Meta:
        model = CampaignAssignment
        fields = '__all__'


class AuditDateSerializer(ModelSerializer):

    class Meta:
        model = AuditDate
        fields = '__all__'


class InventoryActivityImageSerializer(ModelSerializer):
    class Meta:
        model = InventoryActivityImage
        fields = '__all__'


class InventoryActivityAssignmentSerializerWithImages(ModelSerializer):

    images = InventoryActivityImageSerializer(many=True, source='inventoryactivityimage_set')

    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'


class InventoryActivitySerializerWithInventoryAssignmentsAndImages(ModelSerializer):

    inventory_activity_assignment = InventoryActivityAssignmentSerializerWithImages(many=True, source='inventoryactivityassignment_set')

    class Meta:
        model = InventoryActivity
        exclude = ('created_at', 'updated_at')


class ShortlistedInventoryPricingSerializerReadOnly(ModelSerializer):

    inventory_activities = InventoryActivitySerializerWithInventoryAssignmentsAndImages(many=True, source='inventoryactivity_set')
    inventory_type = AdInventoryTypeSerializer(source='ad_inventory_type')
    inventory_duration = DurationTypeSerializer(source='ad_inventory_duration')

    class Meta:
        model = ShortlistedInventoryPricingDetails
        exclude = ('created_at', 'updated_at', 'ad_inventory_type', 'ad_inventory_duration')


class ShortlistedSpacesSerializerReadOnly(ModelSerializer):

    shortlisted_inventories = ShortlistedInventoryPricingSerializerReadOnly(many=True, source='shortlistedinventorypricingdetails_set')

    class Meta:
        model = models.ShortlistedSpaces
        exclude = ('created_at', 'updated_at', 'space_mapping')


class PriceMappingDefaultSerializerReadOnly(ModelSerializer):

    inventory_type = AdInventoryTypeSerializer(source='adinventory_type')
    inventory_duration = DurationTypeSerializer(source='duration_type')

    class Meta:
        model = PriceMappingDefault
        fields = '__all__'


class ShortlistedInventoryPricingSerializerWithShortlistedSpacesReadOnly(ModelSerializer):
    """

    """
    inventory_type = AdInventoryTypeSerializer(source='ad_inventory_type')
    inventory_duration = DurationTypeSerializer(source='ad_inventory_duration')
    shortlisted_supplier = ShortlistedSpacesSerializer(source='shortlisted_spaces')

    class Meta:
        model = ShortlistedInventoryPricingDetails
        fields = '__all__'


class AmenitySerializer(ModelSerializer):

    class Meta:
        model = models.Amenity
        fields = '__all__'


class SupplierAmenitiesMapSerializer(ModelSerializer):

    class Meta:
        model = SupplierAmenitiesMap
        fields = '__all__'
        depth = 1


class InventoryActivityAssignmentWithShortlistedSpaceReadOnly(ModelSerializer):
    inventory_details = ShortlistedInventoryPricingSerializerWithShortlistedSpacesReadOnly(
        source='shortlisted_inventory_details')

    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'


class InventoryActivityImageSerializerReadOnly(ModelSerializer):

    inventory_assignment_details = InventoryActivityAssignmentWithShortlistedSpaceReadOnly(source='inventory_activity_assignment')

    class Meta:
        model = InventoryActivityImage
        fields = '__all__'


class InventoryActivityAssignmentSerializerReadOnly(ModelSerializer):
    """
    Read only serializer for Inventory Activity Assignment Model
    """

    images = InventoryActivityImageSerializer(many=True, source='inventoryactivityimage_set')
    shortlisted_inventory_details = ShortlistedInventoryPricingSerializerWithShortlistedSpacesReadOnly()

    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'


class InventoryActivityAssignmentSerializer(ModelSerializer):
    """
    General serializer for inv act assignment
    """
    class Meta:
        model = InventoryActivityAssignment
        fields = '__all__'


class ObjectLevelPermissionSerializer(ModelSerializer):
    """
    serializer for Object Level Permissions
    """
    class Meta:
        model = models.ObjectLevelPermission
        fields = '__all__'


class GeneralUserPermissionSerializer(ModelSerializer):
    """
    serializer for GeneralUserPermissions
    """
    class Meta:
        model = models.GeneralUserPermission
        fields = '__all__'


class OrganisationSerializer(ModelSerializer):

    class Meta:
        model = models.Organisation
        fields = '__all__'


class ProfileNestedSerializer(ModelSerializer):
    """
    Nested serializer for Profile
    """
    organisation = OrganisationSerializer()
    object_level_permission = ObjectLevelPermissionSerializer(many=True, source='objectlevelpermission_set')
    general_user_permission = GeneralUserPermissionSerializer(many=True, source='generaluserpermission_set')

    class Meta:
        model = models.Profile
        fields = '__all__'


class ProfileSimpleSerializer(ModelSerializer):
    """
    simple serializer for Profile
    """
    class Meta:
        model = models.Profile
        fields = '__all__'



class ContentTypeSerializer(ModelSerializer):

    class Meta:
        model =  ContentType
        fields = '__all__'


class ObjectLevelPermissionViewSet(ModelSerializer):
    """

    """
    class Meta:
        model = models.ObjectLevelPermission
        fields = '__all__'


class RoleSerializer(ModelSerializer):
    """
    simple serializer for Role
    """
    class Meta:
        model = models.Role
        fields = '__all__'

class RoleHierarchySerializer(ModelSerializer):
    """
    simple serializer for RoleHierarchy
    """
    class Meta:
        model = models.RoleHierarchy
        fields = '__all__'

class GenericExportFileSerializer(ModelSerializer):
    """
    simple serializer for generic export file name
    """

    class Meta:
        model = models.GenericExportFileName
        fields = '__all__'

class LeadAliasSerializer(ModelSerializer):
    """
    simple serializer for LeadAlias
    """

    class Meta:
        model = models.LeadAlias
        fields = '__all__'

class LeadsSerializer(ModelSerializer):
    """

    """

    class Meta:
        model = models.Leads
        fields = '__all__'