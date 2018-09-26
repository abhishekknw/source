from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from models import LeadsForm, LeadsFormItems, LeadsFormData, LeadsFormContacts


class LeadsFormSerializer(ModelSerializer):

    class Meta:
        model = LeadsForm
        fields = '__all__'


class LeadsFormItemsSerializer(ModelSerializer):

    class Meta:
        model = LeadsFormItems
        fields = '__all__'


class LeadsFormDataSerializer(ModelSerializer):

    class Meta:
        model = LeadsFormData
        fields = '__all__'

class LeadsFormContactsSerializer(ModelSerializer):

    class Meta:
        model= LeadsFormContacts
        fields = '__all__'
