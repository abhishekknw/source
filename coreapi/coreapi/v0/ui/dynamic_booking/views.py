from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import (BaseBookingTemplate, BookingTemplate, BookingData, BookingDetails, BookingInventoryActivity,
                     BookingInventory)
from datetime import datetime
from bson.objectid import ObjectId
from .utils import validate_booking
from v0.ui.dynamic_suppliers.models import SupplySupplier


class BaseBookingTemplateView(APIView):
    @staticmethod
    def post(request):

        name = request.data['name'] if 'name' in request.data else None
        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        supplier_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        base_supplier_type_id = request.data['base_supplier_type_id'] if 'base_supplier_type_id' in request.data else None
        dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes,
                                  "booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "base_supplier_type_id": base_supplier_type_id}
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
            final_data['supplier_attributes'] = data.supplier_attributes
            final_data['name'] = data.name if 'name' in data else None
            final_data['base_supplier_type_id'] = data.base_supplier_type_id
            final_data['organisation_id'] = data.organisation_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


class BaseBookingTemplateById(APIView):
    @staticmethod
    def get(request, base_booking_template_id):
        base_booking_supplier_type = BaseBookingTemplate.objects.raw({'_id': ObjectId(base_booking_template_id)})[0]
        base_booking_supplier_type = {
            "id": str(base_booking_supplier_type._id),
            "base_supplier_type_id": str(base_booking_supplier_type.base_supplier_type_id),
            "name": base_booking_supplier_type.name,
            "supplier_attributes": base_booking_supplier_type.supplier_attributes,
            "booking_attributes": base_booking_supplier_type.booking_attributes,
            "organisation_id": base_booking_supplier_type.organisation_id
        }
        return handle_response('', data=base_booking_supplier_type, success=True)

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
        supplier_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        base_booking_template_id = request.data['base_booking_template_id'] if 'base_booking_template_id' in request.data else None
        supplier_type_id = request.data['supplier_type_id'] if 'supplier_type_id' in request.data else None
        dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes,
                                  "booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "base_booking_template_id": base_booking_template_id,
                                  "supplier_type_id": supplier_type_id}
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
            final_data['supplier_attributes'] = data.supplier_attributes
            final_data['name'] = data.name if 'name' in data else None
            final_data['supplier_type_id'] = data.supplier_type_id
            final_data['organisation_id'] = data.organisation_id
            final_data['id'] = str(data._id)
            final_data_list.append(final_data)
        return handle_response('', data=final_data_list, success=True)


class BookingTemplateById(APIView):
    @staticmethod
    def get(request, booking_template_id):
        booking_supplier_type = BookingTemplate.objects.raw({'_id': ObjectId(booking_template_id)})[0]
        booking_supplier_type = {
            "id": str(booking_supplier_type._id),
            "supplier_type_id": str(booking_supplier_type.supplier_type_id),
            "name": booking_supplier_type.name,
            "supplier_attributes": booking_supplier_type.supplier_attributes,
            "booking_attributes": booking_supplier_type.booking_attributes,
            "organisation_id": booking_supplier_type.organisation_id

        }
        return handle_response('', data=booking_supplier_type, success=True)

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


def create_inventories(inventory_counts, supplier_id, campaign_id):
    for inventory in inventory_counts:
        for _ in range(inventory["count"]):
            BookingInventory(**{
                "supplier_id": supplier_id,
                "inventory_name": inventory["name"],
                "campaign_id": campaign_id,
                "created_at": datetime.now()
            }).save()


class BookingDataView(APIView):
    @staticmethod
    def post(request):
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None

        data_old_all = BookingData.objects.raw({'campaign_id': campaign_id})
        data_old = None
        if data_old_all and len(list(data_old_all)) > 0:
            data_old = data_old_all[0]
        if data_old:
            old_supplier_id = data_old.supplier_id if 'supplier_id' in data_old else None
            old_booking_template_id= data_old.booking_template_id if 'booking_template_id' in data_old else None

        booking_attributes = request.data['booking_attributes'] if 'booking_attributes' in request.data else None
        comments = request.data['comments'] if 'comments' in request.data else None
        phase_id = int(request.data['phase_id']) if 'phase_id' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        inventory_counts = request.data['inventory_counts'] if 'inventory_counts' in request.data else None
        if inventory_counts:
            create_inventories(inventory_counts, supplier_id, campaign_id)
        if data_old:
            if old_supplier_id == supplier_id:
                return handle_response('', data="supplier_id already exist", success=None)

        booking_template_id = request.data['booking_template_id'] if 'booking_template_id' in request.data else None
        if data_old:
            if old_booking_template_id != booking_template_id:
                return handle_response('', data="booking_template_id must be same for same campaign_id", success=None)

        dict_of_req_attributes = {"booking_attributes": booking_attributes, "organisation_id": organisation_id,
                                  "supplier_id": supplier_id, "campaign_id": campaign_id, "booking_template_id": booking_template_id}

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
        final_data['supplier_attributes'] = get_supplier_attributes(data.supplier_id, booking_template.supplier_attributes)
        final_data['name'] = data.name if 'name' in data else None
        final_data['supplier_id'] = data.supplier_id
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


def get_supplier_attributes(supplier_id, supplier_attributes):
    all_supplier_attribute_names = [supplier['name'] for supplier in supplier_attributes]
    supplier_object = SupplySupplier.objects.raw({"_id": ObjectId(supplier_id)})[0]
    final_attributes = []
    for supplier in supplier_object.supplier_attributes:
        if supplier['name'] in all_supplier_attribute_names:
            final_attributes.append(supplier)
    return final_attributes


class BookingDataByCampaignId(APIView):
    @staticmethod
    def get(request, campaign_id):
        data_all = list(BookingData.objects.raw({'campaign_id': campaign_id}))
        all_supplier_ids = [data.supplier_id for data in data_all]
        booking_template_id = data_all[0].booking_template_id
        booking_template = BookingTemplate.objects.raw({"_id": ObjectId(booking_template_id)})[0]
        final_data_list = []
        for data in data_all:
            final_data = {}
            final_data['booking_attributes'] = data.booking_attributes
            final_data['comments'] = data.comments
            final_data['inventory_counts'] = data.inventory_counts
            final_data['phase_id'] = data.phase_id
            final_data['supplier_attributes'] = get_supplier_attributes(data.supplier_id, booking_template.supplier_attributes)
            final_data['supplier_id'] = data.supplier_id
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
            final_data['supplier_id'] = inventory.supplier_id
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
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        activity_list = request.data['activity_list'] if 'activity_list' in request.data else None
        all_booking_inventories = BookingInventory.objects.raw({"campaign_id": campaign_id,
                                                                "inventory_name": inventory_name,
                                                                "supplier_id": supplier_id})
        all_booking_inventory_ids = [booking_inventory._id for booking_inventory in all_booking_inventories]
        for booking_inventory_id in all_booking_inventory_ids:
            for activity in activity_list:
                assigned_to_id = activity['assigned_to_id'] if 'assigned_to_id' in activity else None
                activity_type = activity['activity_type'] if 'activity_type' in activity else None
                activity_date = activity['activity_date'] if 'activity_date' in activity else None
                comments = request.data['comments'] if 'comments' in request.data else None
                inventory_images = request.data['inventory_images'] if 'inventory_images' in request.data else None
                dict_of_req_attributes = {"booking_inventory_id": booking_inventory_id, "assigned_to_id": assigned_to_id,
                                          "activity_type": activity_type, "activity_date": activity_date,
                                          "campaign_id": campaign_id, "inventory_name": inventory_name,
                                          "supplier_id": supplier_id}

                (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
                if not is_valid:
                    return handle_response('', data=validation_msg_dict, success=None)
                booking_assignment = dict_of_req_attributes
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
            final_data['inventory_name'] = data.inventory_name
            final_data['supplier_id'] = data.supplier_id
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
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        inventory_name = request.data['inventory_name'] if 'inventory_name' in request.data else None
        activity_list = request.data['activity_list'] if 'activity_list' in request.data else None
        for activity in activity_list:
            assigned_to_id = activity['assigned_to_id'] if 'assigned_to_id' in activity else None
            activity_type = activity['activity_type'] if 'activity_type' in activity else None
            activity_date = activity['activity_date'] if 'activity_date' in activity else None
            status = activity['status'] if 'status' in activity else None
            comments = activity['comments'] if 'comments' in activity else None
            update_dict = {}
            if assigned_to_id:
                update_dict["assigned_to_id"] = assigned_to_id
            if activity_type:
                update_dict["activity_type"] = activity_type
            if activity_date:
                update_dict["activity_date"] = activity_date
            if status:
                update_dict["status"] = status
            if comments:
                update_dict["comments"] = comments
            update_dict["updated_at"] = datetime.now()
            BookingInventoryActivity.objects.raw({"campaign_id": campaign_id,"inventory_name": inventory_name,
                                                  "supplier_id": supplier_id}).update({"$set": update_dict})
        return handle_response('', data={"success": True}, success=True)