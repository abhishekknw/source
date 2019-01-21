from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from models import Checklist, ChecklistRows, ChecklistColumns


class ChecklistSerializer(ModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'

