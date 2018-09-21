from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from models import Checklist, ChecklistRows, ChecklistColumns


class ChecklistSerializer(ModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'

class ChecklistColumnsSerializer(ModelSerializer):
    class Meta:
        model = ChecklistColumns
        fields = '__all__'


class ChecklistDataSerializer(ModelSerializer):
    class Meta:
        model = ChecklistColumns
        fields = '__all__'