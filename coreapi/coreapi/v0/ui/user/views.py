from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from v0.ui.common.models import BaseUser
from v0.ui.account.models import Profile
from bson.objectid import ObjectId
from datetime import datetime
from v0.ui.user.serializers import BaseUserSerializer


class UserAPI(APIView):
    @staticmethod
    def get(request):
        organisation_id = get_user_organisation_id(request.user)
        if request.user.is_superuser:
            users = BaseUser.objects.all()
        else:
            users = []
            if organisation_id:
                users = BaseUser.objects.filter(profile__organisation=organisation_id)
        serializer = BaseUserSerializer(users, many=True)
        return handle_response('', data=serializer.data, success=True)


class UserAPISelf(APIView):
    @staticmethod
    def get(request):
        user = request.user
        profile_id = request.user.profile_id
        profile = Profile.objects.filter(id=profile_id).all()[0]
        user = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "profile": {
                "name": profile.name,
                "id": profile.id
            }
        }
        return handle_response('', data=user, success=True)
