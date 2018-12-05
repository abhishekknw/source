from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from models import Notifications
from bson.objectid import ObjectId
from datetime import datetime


class NotificationsAPI(APIView):

    @staticmethod
    def post(request):
        to_id = request.data['to_id'] if 'to_id' in request.data else None
        from_id = request.data['from_id'] if 'from_id' in request.data else None
        notification_msg = request.data['notification_msg'] if 'from_id' in request.data else None
        module_name = request.data['module_name'] if "module_name" in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"to_id": to_id, "from_id": from_id, "notification_msg": notification_msg,
                                  "organisation_id": organisation_id, "module_name": module_name}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        notification_dict = dict_of_req_attributes
        notification_dict["created_at"] = datetime.now()
        Notifications(**notification_dict).save()
        return handle_response('', data={"success": True}, success=True)