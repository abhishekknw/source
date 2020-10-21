from rest_framework.serializers import ModelSerializer
from .models import (BaseUser)
from rest_framework import serializers

class BaseUserSerializer(ModelSerializer):
	
	class Meta:
		model = BaseUser
		fields = '__all__'
		