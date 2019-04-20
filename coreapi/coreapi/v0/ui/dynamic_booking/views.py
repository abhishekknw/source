from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import (BaseBookingTemplate, BookingTemplate, BookingData, BookingDetails, BookingInventoryActivity,
                     BookingInventory)
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


def create_inventories(inventory_counts, entity_id, campaign_id):
    for inventory in inventory_counts:
        for _ in range(inventory["count"]):
            BookingInventory(**{
                "entity_id": entity_id,
                "inventory_name": inventory["name"],
                "campaign_id": campaign_id,
                "created_at": datetime.now()
            }).save()


class BookingDataView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None

        data_old = BookingData.objects.raw({'campaign_id': campaign_id})[0]
        old_entity_id = data_old.entity_id if 'entity_id' in data_old else None
        old_booking_template_id= data_old.booking_template_id if 'booking_template_id' in data_old else None

        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        comments = request.data['comments'] if 'comments' in request.data else None
        phase_id = int(request.data['phase_id']) if 'phase_id' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        entity_id = request.data['entity_id'] if 'entity_id' in request.data else None
        inventory_counts = request.data['inventory_counts'] if 'inventory_counts' in request.data else None
        if inventory_counts:
            create_inventories(inventory_counts, entity_id, campaign_id)
        if old_entity_id == entity_id:
            return handle_response('', data="entity_id already exist", success=None)

        booking_template_id = request.data['booking_template_id'] if 'booking_template_id' in request.data else None
        if old_booking_template_id != booking_template_id:
            return handle_response('', data="booking_template_id must be same for same campaign_id", success=None)

        dict_of_req_attributes = {"booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "entity_id": entity_id, "campaign_id": campaign_id, "booking_template_id": booking_template_id}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=None)
        booking_data = dict_of_req_attributes
        booking_data["created_at"] = datetime.now()
        if comments:
            booking_data["comments"] = comments
        if inventory_counts:
            booking_data["inventory_counts"] = inventory_counts
        if phase_id:
            booking_data["phase_id"] = phase_id
        BookingData(**booking_data).save()
        return handle_response('', data={"success": True}, success=True)


class BookingDataById(APIView):
    @staticmethod
    def get(request, booking_data_id):
        data = BookingData.objects.raw({'_id': ObjectId(booking_data_id)})[0]
        booking_template_id = data.booking_template_id
        booking_template = BookingTemplate.objects.raw({"_id": ObjectId(booking_template_id)})[0]
        final_data = dict()
        final_data['booking_attributes'] = data.booking_attributes
        final_data['comments'] = data.comments
        final_data['inventory_counts'] = data.inventory_counts
        final_data['phase_id'] = data.phase_id
        final_data['entity_attributes'] = get_entity_attributes(data.entity_id, booking_template.entity_attributes)
        final_data['name'] = data.name if 'name' in data else None
        final_data['entity_id'] = data.entity_id
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_template_id'] = data.booking_template_id
        final_data['id'] = str(data._id)
        return handle_response('', data=final_data, success=True)

    @staticmethod
    def put(request, booking_data_id):
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        comments = request.data['comments'] if 'comments' in request.data else None
        inventory_counts = request.data['inventory_counts'] if 'inventory_counts' in request.data else None
        phase_id = request.data['phase_id'] if 'phase_id' in request.data else None
        update_dict = {}
        if booking_attributes:
            update_dict["booking_attributes"] = booking_attributes
        if comments:
            update_dict["comments"] = comments
        if phase_id:
            update_dict["phase_id"] = phase_id
        update_dict["updated_at"] = datetime.now()
        BookingData.objects.raw({'_id': ObjectId(booking_data_id)}).update({"$set": update_dict})
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def delete(request, booking_data_id):
        exist_query = BookingData.objects.raw({'_id': ObjectId(booking_data_id)})
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
            final_data['comments'] = data.comments
            final_data['inventory_counts'] = data.inventory_counts
            final_data['phase_id'] = data.phase_id
            final_data['entity_attributes'] = get_entity_attributes(data.entity_id, booking_template.entity_attributes)
            final_data['entity_id'] = data.entity_id
            final_data['organisation_id'] = data.organisation_id
            final_data['campaign_id'] = data.campaign_id
            final_data['booking_template_id'] = data.booking_template_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)

    @staticmethod
    def delete(request, campaign_id):
        exist_query = BookingData.objects.raw({'campaign_id': campaign_id})
        exist_query.delete()
        return handle_response('', data="success", success=True)


class BookingDetailsView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        booking_template_id = request.data['booking_template_id'] if 'booking_template_id' in request.data else None

        dict_of_req_attributes = {"organisation_id": organisation_id, "campaign_id": campaign_id,
                                  "booking_template_id": booking_template_id}

        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=None)
        booking_data = dict_of_req_attributes
        booking_data["created_at"] = datetime.now()
        BookingDetails(**booking_data).save()
        return handle_response('', data={"success": True}, success=True)


class BookingDetailsById(APIView):
    @staticmethod
    def get(request, booking_details_id):
        data = BookingDetails.objects.raw({'_id': ObjectId(booking_details_id)})[0]
        final_data = dict()
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_template_id'] = data.booking_template_id
        final_data['id'] = str(data._id)
        return handle_response('', data=final_data, success=True)

    @staticmethod
    def delete(request, booking_details_id):
        exist_query = BookingDetails.objects.raw({'_id': ObjectId(booking_details_id)})
        exist_query.delete()
        return handle_response('', data="success", success=True)


class BookingDetailsByCampaignId(APIView):
    @staticmethod
    def get(request, campaign_id):
        data = BookingDetails.objects.raw({'campaign_id': campaign_id})[0]
        final_data = dict()
        final_data['organisation_id'] = data.organisation_id
        final_data['campaign_id'] = data.campaign_id
        final_data['booking_template_id'] = data.booking_template_id
        final_data['id'] = str(data._id)
        return handle_response('', data=final_data, success=True)


class BookingInventoryView(APIView):
    @staticmethod
    def get(request, campaign_id):
        all_inventories = BookingInventory.objects.raw({'campaign_id': campaign_id})
        list_of_inventory_dicts = list()
        for inventory in all_inventories:
            final_data = dict()
            final_data['entity_id'] = inventory.entity_id
            final_data['campaign_id'] = inventory.campaign_id
            final_data['inventory_name'] = inventory.inventory_name
            final_data['comments'] = inventory.comments
            final_data['inventory_images'] = inventory.inventory_images
            final_data['created_at'] = inventory.created_at
            final_data['id'] = str(inventory._id)
            list_of_inventory_dicts.append(final_data)
        return handle_response('', data=list_of_inventory_dicts, success=True)


class BookingAssignmentView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None
        inventory_name = request.data['inventory_name'] if 'inventory_name' in request.data else None
        all_booking_inventories = BookingInventory.objects.raw({"campaign_id": campaign_id,
                                                                "inventory_name": inventory_name})
        all_booking_inventory_ids = [booking_inventory._id for booking_inventory in all_booking_inventories]
        for booking_inventory_id in all_booking_inventory_ids:
            assigned_to_id = request.data['assigned_to_id'] if 'assigned_to_id' in request.data else None
            activity_type = request.data['activity_type'] if 'activity_type' in request.data else None
            activity_date = request.data['activity_date'] if 'activity_date' in request.data else None
            status = request.data['status'] if 'status' in request.data else None
            comments = request.data['comments'] if 'comments' in request.data else None
            inventory_images = request.data['inventory_images'] if 'inventory_images' in request.data else None
            dict_of_req_attributes = {"booking_inventory_id": booking_inventory_id, "assigned_to_id": assigned_to_id,
                                      "activity_type": activity_type, "activity_date": activity_date,
                                      "campaign_id": campaign_id, "inventory_name": inventory_name}

            (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
            if not is_valid:
                return handle_response('', data=validation_msg_dict, success=None)
            booking_assignment = dict_of_req_attributes
            booking_assignment["status"] = status
            booking_assignment["comments"] = comments
            booking_assignment["inventory_images"] = inventory_images
            BookingInventoryActivity(**booking_assignment).save()
        return handle_response('', data={"success": True}, success=True)


class BookingAssignmentByCampaignId(APIView):
    @staticmethod
    def get(request, campaign_id):
        data_all = list(BookingInventoryActivity.objects.raw({'campaign_id': campaign_id}))
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_inventory_id'] = data.booking_inventory_id
            final_data['assigned_to_id'] = data.assigned_to_id
            final_data['activity_type'] = data.activity_type
            final_data['activity_date'] = data.activity_date
            final_data['actual_activity_date'] = data.actual_activity_date
            final_data['status'] = data.status
            final_data['comments'] = data.comments
            final_data['inventory_images'] = data.inventory_images
            final_data['organisation_id'] = data.organisation_id
            final_data['created_at'] = data.created_at
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


    @staticmethod
    def put(request, campaign_id):
        inventory_name = request.data['inventory_name'] if 'inventory_name' in request.data else None
        assigned_to_id = request.data['assigned_to_id'] if 'assigned_to_id' in request.data else None
        activity_type = request.data['activity_type'] if 'activity_type' in request.data else None
        activity_date = request.data['activity_date'] if 'activity_date' in request.data else None
        status = request.data['status'] if 'status' in request.data else None
        update_dict = {}
        if assigned_to_id:
            update_dict["assigned_to_id"] = assigned_to_id
        if activity_type:
            update_dict["activity_type"] = activity_type
        if activity_date:
            update_dict["activity_date"] = activity_date
        if status:
            update_dict["status"] = status
        update_dict["updated_at"] = datetime.now()
        BookingInventoryActivity.objects.raw({"campaign_id": campaign_id,"inventory_name": inventory_name}).update({"$set": update_dict})
        return handle_response('', data={"success": True}, success=True)