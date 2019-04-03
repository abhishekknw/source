from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import BaseBookingTemplate, BookingTemplate, BookingData
from datetime import datetime
from bson.objectid import ObjectId
from .utils import validate_booking
from v0.ui.dynamic_entities.models import SupplyEntity


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
        data_all = BaseBookingTemplate.objects.raw({})
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_attributes'] = data.booking_attributes
            final_data['entity_attributes'] = data.entity_attributes
            final_data['name'] = data.name if 'name' in data else None
            final_data['base_entity_type_id'] = data.base_entity_type_id
            final_data['organisation_id'] = data.organisation_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


class BaseBookingTemplateById(APIView):
    @staticmethod
    def get(request, base_booking_template_id):
        base_booking_entity_type = BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)})[0]
        base_booking_entity_type = {
            "id": str(base_booking_entity_type._id),
            "base_entity_type_id": str(base_booking_entity_type.base_entity_type_id),
            "name": base_booking_entity_type.name,
            "entity_attributes": base_booking_entity_type.entity_attributes,
            "booking_attributes": base_booking_entity_type.booking_attributes,
            "organisation_id": base_booking_entity_type.organisation_id
        }
        return handle_response('', data=base_booking_entity_type, success=True)

    @staticmethod
    def put(request, base_booking_template_id):
        data = request.data.copy()
        data['updated_at'] = datetime.now()
        BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)}).update({"$set": data})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request, base_booking_template_id):
        exist_query = BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)})
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
        is_valid_adv, validation_msg_dict_adv = validate_booking(booking_template)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        BookingTemplate(**booking_template).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        organisation_id = get_user_organisation_id(request.user)
        data_all = BookingTemplate.objects.raw({'organisation_id':organisation_id})
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_attributes'] = data.booking_attributes
            final_data['entity_attributes'] = data.entity_attributes
            final_data['name'] = data.name if 'name' in data else None
            final_data['entity_type_id'] = data.entity_type_id
            final_data['organisation_id'] = data.organisation_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


class BookingTemplateById(APIView):
    @staticmethod
    def get(request, booking_template_id):
        booking_entity_type = BookingTemplate.objects.raw({'_id': ObjectId(booking_template_id)})[0]
        booking_entity_type = {
            "id": str(booking_entity_type._id),
            "entity_type_id": str(booking_entity_type.entity_type_id),
            "name": booking_entity_type.name,
            "entity_attributes": booking_entity_type.entity_attributes,
            "booking_attributes": booking_entity_type.booking_attributes,
            "organisation_id": booking_entity_type.organisation_id

        }
        return handle_response('', data=booking_entity_type, success=True)

    @staticmethod
    def put(request, booking_template_id):
        data = request.data.copy()
        data['updated_at'] = datetime.now()
        BookingTemplate.objects.raw({'_id': ObjectId(booking_template_id)}).update({"$set": data})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request, booking_template_id):
        exist_query = BookingTemplate.objects.raw({'_id': ObjectId(booking_template_id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)


class BookingDataView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        entity_id = request.data['entity_id'] if 'entity_id' in request.data else None
        booking_template_id = request.data['booking_template_id'] if 'booking_template_id' in request.data else None

        dict_of_req_attributes = {"booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "entity_id": entity_id, "campaign_id": campaign_id, "booking_template_id": booking_template_id}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=None)
        booking_data = dict_of_req_attributes
        booking_data["created_at"] = datetime.now()
        BookingData(**booking_data).save()
        return handle_response('', data={"success": True}, success=True)



class BookingDataById(APIView):
    @staticmethod
    def get(request, booking_id):
        data = BookingData.objects.raw({'_booking_id': ObjectId(booking_id)})
        final_data = dict()
        final_data['booking_attributes'] = data.booking_attributes
        final_data['entity_attributes'] = data.entity_attributes
        final_data['name'] = data.name if 'name' in data else None
        final_data['entity_id'] = data.entity_id
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_id'] = data.booking_id
        return handle_response('', data=final_data, success=True)

    @staticmethod
    def put(request, booking_id):
        data = request.data.copy()
        data['updated_at'] = datetime.now()
        BookingTemplate.objects.raw({'_id': ObjectId(booking_id)}).update({"$set": data})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request, booking_id):
        exist_query = BookingData.objects.raw({'_booking_id': ObjectId(booking_id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)


def get_entity_attributes(entity_id, entity_attributes):
    all_entity_attribute_names = [entity['name'] for entity in entity_attributes]
    entity_object = SupplyEntity.objects.raw({"_id": ObjectId(entity_id)})[0]
    final_attributes = []
    for entity in entity_object.entity_attributes:
        if entity['name'] in all_entity_attribute_names:
            final_attributes.append(entity)
    return final_attributes


class BookingDataByCampaignId(APIView):
    @staticmethod
    def get(request, campaign_id):
        data_all = list(BookingData.objects.raw({'campaign_id': campaign_id}))
        all_entity_ids = [data.entity_id for data in data_all]
        booking_template_id = data_all[0].booking_template_id
        booking_template = BookingTemplate.objects.raw({"_id": ObjectId(booking_template_id)})[0]
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_attributes'] = data.booking_attributes
            final_data['entity_attributes'] = get_entity_attributes(data.entity_id, booking_template.entity_attributes)
            final_data['entity_id'] = data.entity_id
            final_data['organisation_id'] = data.organisation_id
            final_data['campaign_id'] = data.campaign_id
            final_data['booking_template_id'] = data.booking_template_id
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)

    @staticmethod
    def delete(request, campaign_id):
        exist_query = BookingData.objects.raw({'_campaign_id': ObjectId(campaign_id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)

