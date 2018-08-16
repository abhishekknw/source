from rest_framework.serializers import ModelSerializer
from v0.ui.base.serializers import BaseModelPermissionSerializer
from v0.ui.proposal.models import (ProposalInfo, ProposalCenterMappingVersion, ProposalMasterCost, ProposalInfoVersion,
    ProposalMetrics, ProposalCenterMapping, ImageMapping, SpaceMapping, SpaceMappingVersion, ShortlistedSpacesVersion,
                                   HashTagImages)
from rest_framework import serializers
from v0.ui.supplier.models import SupplierTypeSociety, SupplierTypeCorporate

class ShortlistedSpacesVersionSerializer(ModelSerializer):

    class Meta:
        model = ShortlistedSpacesVersion
        fields = '__all__'

class ProposalInfoSerializer(BaseModelPermissionSerializer):

    class Meta:
        model = ProposalInfo
        fields = '__all__'

class ProposalCenterMappingSerializer(ModelSerializer):
    # using this serializer to save the center object
    class Meta:
        model = ProposalCenterMapping
        fields = '__all__'
        # fields = ('proposal', 'center_name', 'id')

class ProposalCenterMappingVersionSerializer(ModelSerializer):

    class Meta:
        model = ProposalCenterMappingVersion
        fields = '__all__'

class ProposalInfoVersionSerializer(ModelSerializer):

    class Meta:
        model = ProposalInfoVersion
        fields = '__all__'

class ProposalMasterCostSerializer(ModelSerializer):
    class Meta:
        model = ProposalMasterCost
        fields = '__all__'

class ProposalMetricsSerializer(ModelSerializer):
    class Meta:
        model = ProposalMetrics
        fields = '__all__'

class ImageMappingSerializer(ModelSerializer):
    class Meta:
        model = ImageMapping
        fields = '__all__'

class SpaceMappingVersionSerializer(ModelSerializer):
    class Meta:
        model = SpaceMappingVersion
        fields = '__all__'

class SpaceMappingSerializer(ModelSerializer):

    class Meta:
        model = SpaceMapping
        fields = '__all__'

class ProposalCenterMappingVersionSpaceSerializer(ModelSerializer):
    # this serializer is used to send data to front end with space_mappings objects
    # Not using to save them
    space_mappings = SpaceMappingVersionSerializer(source='get_space_mappings_versions')

    class Meta:
        model = ProposalCenterMappingVersion
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
class HashtagImagesSerializer(ModelSerializer):
    """
simple serializer for HashtagImages
    """

    class Meta:
        model = HashTagImages