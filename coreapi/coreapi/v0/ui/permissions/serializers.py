from rest_framework.serializers import ModelSerializer
from v0.ui.permissions.models import UserInquiry

class UserInquirySerializer(ModelSerializer):
    class Meta:
        model = UserInquiry
        fields = '__all__'