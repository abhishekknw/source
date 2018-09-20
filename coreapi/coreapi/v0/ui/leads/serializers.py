from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from models import Leads, LeadAlias, LeadsForm, LeadsFormItems, LeadsFormData, LeadsFormContacts


class LeadsSerializer(ModelSerializer):
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
