from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.ui.finances.models import AssignedAudits, Audits
from v0.ui.serializers import UISocietySerializer
from v0.ui.campaign.serializers import CampaignSerializer, CampaignTypeMappingSerializer
from v0.ui.inventory.models import SocietyInventoryBooking



class AssignedAuditSerializer(ModelSerializer):
    type = CampaignTypeMappingSerializer(source='get_type')
    society = UISocietySerializer(source='get_society')
    audit_type = serializers.CharField(source='get_audit_type')
    submit_status = serializers.CharField(source='get_status')

    class Meta:
        model = SocietyInventoryBooking
        read_only_fields = (
        'type'
        'society',
        'audit_type',
        'submit_status'

        )

class AuditSerializer(ModelSerializer):

    class Meta:
        model = Audits


class AssignedAuditsTempSerializer(ModelSerializer):

    class Meta:
        model = AssignedAudits

