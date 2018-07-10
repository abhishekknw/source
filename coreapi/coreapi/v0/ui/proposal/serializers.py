from rest_framework.serializers import ModelSerializer
from v0.ui.base.serializers import BaseModelPermissionSerializer
from v0.ui.proposal.models import (ProposalInfo, ProposalCenterMappingVersion, ProposalMasterCost, ProposalInfoVersion,
    ProposalMetrics, ProposalCenterMapping)

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