from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import BaseBookingTemplate, BookingTemplate
from datetime import datetime
from bson.objectid import ObjectId


class BaseBookingTemplateView(APIView):
    @staticmethod
    def post(request):

        name = request.data['name'] if 'name' in request.data else None
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        entity_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        base_entity_type_id = request.data['base_entity_type_id'] if 'base_entity_type_id' in request.data else None
        dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes,
                                  "booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "base_entity_type_id": base_entity_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:

            return handle_response('', data=validation_msg_dict, success=None)
        base_booking_template = dict_of_req_attributes
        base_booking_template["created_at"] = datetime.now()
        BaseBookingTemplate(**base_booking_template).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        organisation_id = request.user.profile.organisation.organisation_id
        final_data = {}
        data_all = BaseBookingTemplate.objects.raw({})
        final_data_list = []
        for data in data_all:
            final_data = {}
            if 'booking_attributes' in data:
                final_data['booking_attributes'] = []
                for item in data.booking_attributes:
                    temp_data = {
                        "name": item['name'] if item['name'] else None,
                        "type": item['type'] if item['type'] else None,
                        "is_required": item['is_required'] if 'is_required' in item else None
                    }
                    if 'options' in item:
                        temp_data['options'] = []
                        for option in item['options']:
                            temp_data['options'].append(option)
                    final_data['booking_attributes'].append(temp_data)
            if 'entity_attributes' in data:
                final_data['entity_attributes'] = []
                for item in data.entity_attributes:
                    temp_data = {
                        "name": item['name'] if item['name'] else None,
                        "is_required": item['is_required'] if 'is_required' in item else None
                    }
                    final_data['entity_attributes'].append(temp_data)

            final_data['name'] = data.name if 'name' in data else None
            final_data['base_entity_type_id'] = data.base_entity_type_id
            final_data['organisation_id'] = data.organisation_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)

    @staticmethod
    def put(request):
        id = request.query_params.get('id', None)
        data = request.data.copy()
        data.pop('id')
        data['updated_at'] = datetime.now()
        BaseBookingTemplate.objects.raw({'_id': ObjectId(id)}).update({"$set": data})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request):
        id = request.query_params.get("id", None)
        if not id:
            return handle_response('', data="Id Not Provided", success=False)
        exist_query = BaseBookingTemplate.objects.raw({'_id': ObjectId(id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)

class BookingTemplateView(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        entity_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        base_booking_template_id = request.data['base_booking_template_id'] if 'base_booking_template_id' in request.data else None
        entity_type_id = request.data['entity_type_id'] if 'entity_type_id' in request.data else None
        dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes,
                                  "booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "base_booking_template_id": base_booking_template_id,
                                  "entity_type_id": entity_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:

            return handle_response('', data=validation_msg_dict, success=False)
        booking_template = dict_of_req_attributes
        booking_template["created_at"] = datetime.now()
        BookingTemplate(**booking_template).save()
        return handle_response('', data={"success": True}, success=True)
