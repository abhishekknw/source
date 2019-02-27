from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import BaseBookingTemplate
from datetime import datetime


class BaseBookingTemplateView(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else False
        entity_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else False
        organisation_id = get_user_organisation_id(request.user)
        base_entity_type_id = request.data['base_entity_type_id'] if 'base_entity_type_id' in request.data else False
        dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes,
                                  "booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "base_entity_type_id": base_entity_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:

            return handle_response('', data=validation_msg_dict, success=False)
        base_booking_template = dict_of_req_attributes
        base_booking_template["created_at"] = datetime.now()
        BaseBookingTemplate(**base_booking_template).save()
        return handle_response('', data={"success": True}, success=True)
