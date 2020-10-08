from rest_framework.serializers import ModelSerializer
from v0.ui.account.serializers import ContactDetailsSerializer
from .models import (Requirement)

class RequirementSerializer(ModelSerializer):
    lead_by = ContactDetailsSerializer()
    class Meta:
        model = Requirement
        fields = '__all__'