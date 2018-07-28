from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from models import Lead, Leads, CampaignLeads, LeadAlias, SocietyLeads

class LeadSerializer(ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class LeadsSerializer(ModelSerializer):
    """

    """

    class Meta:
        model = Leads
        fields = '__all__'

class LeadAliasSerializer(ModelSerializer):
    """
    simple serializer for LeadAlias
    """

    class Meta:
        model = LeadAlias
        fields = '__all__'