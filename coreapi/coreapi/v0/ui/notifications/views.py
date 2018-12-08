from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from models import Notifications
from bson.objectid import ObjectId
from datetime import datetime


def create_new_notification(user, to_id, from_id, notification_msg, module_name):
    organisation_id = get_user_organisation_id(user)
    dict_of_req_attributes = {"to_id": to_id, "from_id": from_id, "notification_msg": notification_msg,
                              "organisation_id": organisation_id, "module_name": module_name}
    (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
    if not is_valid:
        return is_valid, validation_msg_dict
    notification_dict = dict_of_req_attributes
    notification_dict["created_at"] = datetime.now()
    Notifications(**notification_dict).save()
    return is_valid, validation_msg_dict


class NotificationsAPI(APIView):

    @staticmethod
    def post(request):
        to_id = request.data['to_id'] if 'to_id' in request.data else None
        from_id = request.data['from_id'] if 'from_id' in request.data else None
        notification_msg = request.data['notification_msg'] if 'from_id' in request.data else None
        module_name = request.data['module_name'] if "module_name" in request.data else None
        is_valid, validation_msg_dict = create_new_notification(request.user, to_id, from_id, notification_msg, module_name)
        if not is_valid:
            handle_response('', data=validation_msg_dict, success=False)
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        to_id = request.user.id
        from_id = request.query_params.get("from_id", None)
        is_read = request.query_params.get("is_read", None)
        filter_object = {"to_id":to_id}
        if from_id:
            filter_object["from_id"] = from_id
        if is_read:
            filter_object["is_read"] = True if is_read.lower() == "true" else False
        all_notifications = Notifications.objects.raw(filter_object)
        all_notifications_dict = {}
        for notification in all_notifications:
            all_notifications_dict[str(notification._id)] = {
                "id": str(notification._id),
                "notification_msg": notification.notification_msg,
                "to_id": notification.to_id,
                "from_id": notification.from_id,
                "module_name": notification.module_name,
                "created_at": notification.created_at,
            }
        return handle_response('', data=all_notifications_dict, success=True)


class NotificationsMarkReadAPI(APIView):
    @staticmethod
    def put(request, notification_id):
        notification_dict = {"is_read": True, "updated_at": datetime.now()}
        Notifications.objects.raw({'_id': ObjectId(notification_id)}).update({"$set": notification_dict})
        return handle_response('', data={"success": True}, success=True)