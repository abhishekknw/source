from rest_framework.serializers import ModelSerializer
from v0.ui.account.serializers import ContactDetailsSerializer
from .models import (Requirement, PreRequirement)
from rest_framework import serializers
from v0.ui.common.models import BaseUser



class RequirementSerializer(ModelSerializer):

	lead_by = ContactDetailsSerializer(read_only=True)
	class Meta:
		model = Requirement
		fields = '__all__'

class PreRequirementSerializer(ModelSerializer):

	lead_by = ContactDetailsSerializer(read_only=True)
	class Meta:
		model = PreRequirement
		fields = '__all__'