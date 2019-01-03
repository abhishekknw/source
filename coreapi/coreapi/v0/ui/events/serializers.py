from __future__ import absolute_import
from rest_framework.serializers import ModelSerializer
from .models import Events, SocietyMajorEvents

class EventsSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class SocietyMajorEventsSerializer(ModelSerializer):
    class Meta:
        model = SocietyMajorEvents
        fields = '__all__'