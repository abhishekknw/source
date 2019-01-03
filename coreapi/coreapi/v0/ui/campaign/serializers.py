from __future__ import absolute_import
from rest_framework.serializers import ModelSerializer
from .models import (Campaign, CampaignSupplierTypes, CampaignTypeMapping, CampaignSocietyMapping, CampaignAssignment,
                    GenericExportFileName)
from rest_framework import serializers
from v0.ui.user.serializers import BaseUserSerializer
from v0.ui.proposal.serializers import ProposalInfoSerializer

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

class CampaignAssignmentSerializerReadOnly(ModelSerializer):

    assigned_by = BaseUserSerializer()
    assigned_to = BaseUserSerializer()
    campaign = ProposalInfoSerializer()

    class Meta:
        model = CampaignAssignment
        fields = '__all__'


class CampaignAssignmentSerializer(ModelSerializer):

    class Meta:
        model = CampaignAssignment
        fields = '__all__'


class GenericExportFileSerializer(ModelSerializer):
    """
    simple serializer for generic export file name
    """

    class Meta:
        model = GenericExportFileName
        fields = '__all__'