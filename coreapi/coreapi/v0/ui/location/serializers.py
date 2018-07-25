from rest_framework.serializers import ModelSerializer
from models import City, CityArea, CitySubArea, State, ImageMapping

class CitySubAreaSerializer(ModelSerializer):
    class Meta:
        model = CitySubArea
        fields = '__all__'


class CityAreaSerializer(ModelSerializer):
    class Meta:
        model = CityArea
        fields = '__all__'


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class StateSerializer(ModelSerializer):

    class Meta:
        model = State

class ImageMappingSerializer(ModelSerializer):
    class Meta:
        model = ImageMapping
        fields = '__all__'