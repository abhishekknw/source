from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from v0.ui.common.models import BaseUser
from v0.ui.account.models import Profile
from bson.objectid import ObjectId
from datetime import datetime


class UserAPI(APIView):

    @staticmethod
    def get(request):
        organisation_id = get_user_organisation_id(request.user)
        all_profiles = Profile.objects.filter(organisation_id=organisation_id).all()
        all_profile_ids = [profile.id for profile in all_profiles]
        all_users = BaseUser.objects.filter(profile_id__in=all_profile_ids).all()
        all_user_list = [{"first_name": user.first_name,
                                   "last_name": user.last_name,
                                   "username": user.username,
                                   "email": user.email,
                                   "id": user.id
                                   } for user in all_users]
        return handle_response('', data=all_user_list, success=True)


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
