from rest_framework.serializers import ModelSerializer
from models import CommunityHallInfo, LiftDetails, NoticeBoardDetails, SocietyFlat, FlatType, \
    SwimmingPoolInfo, MailboxInfo, SportsInfra, SocietyTower, CommonAreaDetails
from rest_framework import serializers

class CommunityHallInfoSerializer(ModelSerializer):
    class Meta:
        model = CommunityHallInfo
        fields = '__all__'

class LiftDetailsSerializer(ModelSerializer):
    tower_name = serializers.CharField(source='get_tower_name')

    class Meta:
        model = LiftDetails
        fields = '__all__'
        read_only_fields = (
            'tower_name'
        )

class NoticeBoardDetailsSerializer(ModelSerializer):
    tower_name = serializers.CharField(source='get_tower_name')

    class Meta:
        model = NoticeBoardDetails
        fields = '__all__'
        read_only_fields = (
            'tower_name'
        )


class SocietyFlatSerializer(ModelSerializer):
    class Meta:
        model = SocietyFlat
        fields = '__all__'


class SwimmingPoolInfoSerializer(ModelSerializer):
    class Meta:
        model = SwimmingPoolInfo
        fields = '__all__'

class CommonAreaDetailsSerializer(ModelSerializer):
    class Meta:
        model = CommonAreaDetails
        fields = '__all__'

class SportsInfraSerializer(ModelSerializer):
    class Meta:
        model = SportsInfra
        fields = '__all__'

class SocietyTowerSerializer(ModelSerializer):
    class Meta:
        model = SocietyTower
        fields = '__all__'

class FlatTypeSerializer(ModelSerializer):
    class Meta:
        model = FlatType
        fields = '__all__'

class MailboxInfoSerializer(ModelSerializer):
    class Meta:
        model = MailboxInfo
        fields = '__all__'