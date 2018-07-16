from rest_framework.serializers import ModelSerializer
from models import DoorToDoorInfo

class DoorToDoorInfoSerializer(ModelSerializer):
    class Meta:
        model = DoorToDoorInfo
        fields = '__all__'