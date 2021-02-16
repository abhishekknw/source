from rest_framework.serializers import ModelSerializer
from v0.ui.account.serializers import ContactDetailsSerializer
from .models import (NotificationTemplates,PaymentDetails,Requirement, PreRequirement,MachadaloRelationshipManager,LicenseDetails)
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

class RelationshipManagerSerializer(ModelSerializer):

	class Meta:
		model = MachadaloRelationshipManager
		fields = '__all__'

class LicenseDetailsSerializer(ModelSerializer):

	class Meta:
		model = LicenseDetails
		fields = '__all__'

class PaymentDetailsSerializer(ModelSerializer):

	class Meta:
		model = PaymentDetails
		fields = '__all__'

class NotificationTemplateSerializer(ModelSerializer):

	class Meta:
		model = NotificationTemplates
		fields = '__all__'