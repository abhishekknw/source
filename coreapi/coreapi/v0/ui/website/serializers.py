from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from v0.models import Business, BusinessContact
from v0.serializers import BusinessSerializer, BusinessContactSerializer

class UIBusinessSerializer(ModelSerializer):
    contact = BusinessContactSerializer(source='get_contact')

    class Meta:
        model = Business
        read_only_fields = (
        'contact'
        )


