from rest_framework.serializers import ModelSerializer
from v0.ui.account.serializers import ContactDetailsSerializer
from .models import (Requirement)
from rest_framework import serializers
from v0.ui.common.models import BaseUser



class RequirementSerializer(ModelSerializer):
	
	lead_by_name = serializers.ReadOnlyField(source="lead_by.name")
	class Meta:
		model = Requirement
		fields = '__all__'