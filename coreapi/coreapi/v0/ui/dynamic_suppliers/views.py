from __future__ import absolute_import
import redis
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import BaseSupplySupplierType, SupplySupplierType, SupplySupplier
from bson.objectid import ObjectId
from datetime import datetime
from .utils import validate_supplier_type_data, validate_with_supplier_type
from v0.ui.supplier.models import (SupplierTypeSociety)
from v0.ui.proposal.models import (ShortlistedSpaces)
from v0.ui.inventory.serializers import (ShortlistedSpacesSerializer, ShortlistedInventoryPricingDetailsSerializer)
from v0.ui.dynamic_booking.models import BookingData, BookingInventoryActivity
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2
from v0.ui.dynamic_booking.models import BaseBookingTemplate, BookingTemplate, BookingData, BookingInventory
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.inventory.models import InventoryActivityImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_paginated_result(data, entries, page):
    paginator = Paginator(data, entries)
    try:
        result = paginator.page(int(page))
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result

class SupplierType(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else False
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        supplier_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else False
        organisation_id = get_user_organisation_id(request.user)
        base_supplier_type_id = request.data['base_supplier_type_id'] if 'base_supplier_type_id' in request.data else False
        dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes,
                                  "organisation_id": organisation_id, "base_supplier_type_id": base_supplier_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_type_dict = dict_of_req_attributes
        supplier_type_dict["is_global"] = is_global
        supplier_type_dict["created_at"] = datetime.now()
        supplier_type_dict["inventory_list"] = request.data['inventory_list'] if 'inventory_list' in request.data else []
        supplier_type_dict["additional_attributes"] = request.data[
            'additional_attributes'] if 'additional_attributes' in request.data else {}
        is_valid_adv, validation_msg_dict_adv = validate_supplier_type_data(supplier_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplySupplierType(**supplier_type_dict).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        all_supply_supplier_type = SupplySupplierType.objects.all()
        all_supply_supplier_type_dict = {}
        for supply_supplier_type in all_supply_supplier_type:
            all_supply_supplier_type_dict[str(supply_supplier_type._id)] = {
                "id": str(supply_supplier_type._id),
                "base_supplier_type_id": str(supply_supplier_type.base_supplier_type_id),
                "name": supply_supplier_type.name,
                "supplier_attributes": supply_supplier_type.supplier_attributes,
                "inventory_list":supply_supplier_type.inventory_list,
                "additional_attributes": supply_supplier_type.additional_attributes
            }
        return handle_response('', data=all_supply_supplier_type_dict, success=True)


class SupplierTypeById(APIView):
    @staticmethod
    def get(request, supplier_type_id):
        supply_supplier_type = SupplySupplierType.objects.raw({'_id':ObjectId(supplier_type_id)})[0]
        supply_supplier_type = {
            "id": str(supply_supplier_type._id),
            "base_supplier_type_id": str(supply_supplier_type.base_supplier_type_id),
            "name": supply_supplier_type.name,
            "supplier_attributes": supply_supplier_type.supplier_attributes,
            "inventory_list": supply_supplier_type.inventory_list,
            "additional_attributes": supply_supplier_type.additional_attributes
        }
        return handle_response('', data=supply_supplier_type, success=True)


    @staticmethod
    def put(request, supplier_type_id):
        new_name = request.data['name'] if 'name' in request.data else None
        new_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        base_supplier_type_id = request.data['base_supplier_type_id'] if 'base_supplier_type_id' in request.data else False
        dict_of_req_attributes = {"name": new_name, "supplier_attributes": new_attributes,
                                  "base_supplier_type_id": base_supplier_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_type_dict = dict_of_req_attributes
        supplier_type_dict["is_global"] = is_global
        supplier_type_dict["updated_at"] = datetime.now()
        if 'inventory_list' in request.data:
            supplier_type_dict["inventory_list"] = request.data['inventory_list']
        if 'additional_attributes' in request.data:
            supplier_type_dict["additional_attributes"] = request.data['additional_attributes']
        is_valid_adv, validation_msg_dict_adv = validate_supplier_type_data(supplier_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        print(supplier_type_dict)
        SupplySupplierType.objects.raw({'_id': ObjectId(supplier_type_id)}).update({"$set": supplier_type_dict})
        return handle_response('', data="success", success=True)


    @staticmethod
    def delete(request, supplier_type_id):
        exist_supplier_query = SupplySupplierType.objects.raw({'_id': ObjectId(supplier_type_id)})[0]
        exist_supplier_query.delete()
        return handle_response('', data="success", success=True)


class Supplier(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        supplier_type_id = request.data['supplier_type_id'] if 'supplier_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        supplier_attributes = request.data['supplier_attributes']
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "supplier_type_id": supplier_type_id, "is_custom": is_custom,
                                  "supplier_attributes": supplier_attributes, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_dict = dict_of_req_attributes
        supplier_dict['created_by'] = request.user.id
        supplier_dict['created_at'] = datetime.now()
        supplier_dict["inventory_list"] = request.data['inventory_list'] if 'inventory_list' in request.data else []
        supplier_dict["additional_attributes"] = request.data['additional_attributes'] if 'additional_attributes' in request.data else {}


        (is_valid_adv, validation_msg_dict_adv) = validate_with_supplier_type(supplier_dict,supplier_type_id)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplySupplier(**supplier_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_supply_supplier = SupplySupplier.objects.all()

        page = request.query_params.get('page', 1)
        entries = 10000
        suppliers = get_paginated_result(all_supply_supplier, entries, page)

        all_supply_supplier_dict = {}
        for supply_supplier in suppliers:
            all_supply_supplier_dict[str(supply_supplier._id)] = {
                "id": str(supply_supplier._id),
                "supplier_type_id": str(supply_supplier.supplier_type_id),
                "name": supply_supplier.name,
                "supplier_attributes": supply_supplier.supplier_attributes,
                "additional_attributes": supply_supplier.additional_attributes,
                "inventory_list": supply_supplier.inventory_list,
                "is_custom": supply_supplier.is_custom,
                "organisation_id": supply_supplier.organisation_id,
                "created_by": supply_supplier.created_by,
                "created_at": supply_supplier.created_at,
            }
        return handle_response('', data=all_supply_supplier_dict, success=True)


class SupplierById(APIView):
    @staticmethod
    def get(request, supplier_id):
        supply_supplier = SupplySupplier.objects.raw({'_id':ObjectId(supplier_id)})[0]
        supply_supplier = {
            "id": str(supply_supplier._id),
            "supplier_type_id": str(supply_supplier.supplier_type_id),
            "name": supply_supplier.name,
            "supplier_attributes": supply_supplier.supplier_attributes,
            "additional_attributes": supply_supplier.additional_attributes,
            "inventory_list": supply_supplier.inventory_list,
            "is_custom": supply_supplier.is_custom,
            "organisation_id": supply_supplier.organisation_id,
            "created_by": supply_supplier.created_by,
            "created_at": supply_supplier.created_at,
        }
        return handle_response('', data=supply_supplier, success=True)

    @staticmethod
    def put(request, supplier_id):
        name = request.data['name'] if 'name' in request.data else None
        supplier_type_id = request.data['supplier_type_id'] if 'supplier_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        supplier_attributes = request.data['supplier_attributes']
        additional_attributes = request.data['additional_attributes']
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "supplier_type_id": supplier_type_id, "is_custom": is_custom,
                                  "supplier_attributes": supplier_attributes, "organisation_id": organisation_id,
                                  "additional_attributes": additional_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_dict = dict_of_req_attributes
        supplier_dict['updated_at'] = datetime.now()
        if 'inventory_list' in request.data:
            supplier_dict["inventory_list"] = request.data['inventory_list']
        (is_valid_adv, validation_msg_dict_adv) = validate_with_supplier_type(supplier_dict, supplier_type_id)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplySupplier.objects.raw({'_id': ObjectId(supplier_id)}).update({"$set": supplier_dict})
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, supplier_id):
        exist_supplier_query = SupplySupplier.objects.raw({'_id': ObjectId(supplier_id)})[0]
        exist_supplier_query.delete()
        return handle_response('', data="success", success=True)


class SupplierTransfer(APIView):
    @staticmethod
    def get(request):
        supplier_objects = SupplierTypeSociety.objects.all()
        serializer = SupplierTypeSocietySerializer(supplier_objects, many=True)
        society_list = serializer.data
        new_base_supplier_for_society = BaseSupplySupplierType(**{
            "name": "Base Society",
            "supplier_attributes": [{"name":"supplier_id","type": "STRING"},
                                  {"name":"name","type": "STRING"},
                                  {"name":"society_address1","type": "STRING"},
                                  {"name":"society_address2","type": "STRING"},
                                  {"name":"society_zip","type": "STRING"},
                                  {"name":"society_name","type": "STRING"},
                                  {"name":"society_city","type": "STRING"},
                                  {"name":"society_state", "type": "STRING"},
                                  {"name":"society_longitude", "type": "STRING"},
                                  {"name":"society_locality", "type": "STRING"},
                                  {"name": "society_subarea", "type": "STRING"},
                                  {"name": "society_latitude", "type": "STRING"},
                                  {"name": "society_location_type", "type": "STRING"},
                                  {"name": "society_type_quality", "type": "STRING"},
                                  {"name": "society_type_quantity", "type": "STRING"},
                                  {"name": "flat_count", "type": "STRING"},
                                  {"name": "flat_avg_rental_persqft", "type": "STRING"},
                                  {"name": "flat_sale_cost_persqft", "type": "STRING"},
                                  {"name": "tower_count", "type": "INT"},
                                  {"name": "payment_details_available", "type": "BOOLEAN"},
                                  {"name": "age_of_society", "type": "INT"},
                                  {"name": "total_tenant_flat_count", "type": "INT"},
                                  {"name": "landmark", "type": "STRING"},
                                  {"name": "name_for_payment", "type": "STRING"},
                                  {"name": "bank_name", "type": "STRING  "},
                                  {"name": "ifsc_code", "type": "STRING"},
                                  {"name": "account_no", "type": "STRING"},
                              {"name": "representative", "type": "STRING"}],
        }).save()
        base_supplier_for_society_id = new_base_supplier_for_society._id
        new_supplier_type_for_society = SupplySupplierType(**{
            "name": "Base Society",
            "base_supplier_type_id": base_supplier_for_society_id,
            "supplier_attributes": [{"name": "supplier_id", "type": "STRING"},
                                  {"name": "name", "type": "STRING"},
                                  {"name": "society_address1", "type": "STRING"},
                                  {"name": "society_address2", "type": "STRING"},
                                  {"name": "society_zip", "type": "STRING"},
                                  {"name": "society_name", "type": "STRING"},
                                  {"name": "society_city", "type": "STRING"},
                                  {"name": "society_state", "type": "STRING"},
                                  {"name": "society_longitude", "type": "STRING"},
                                  {"name": "society_locality", "type": "STRING"},
                                  {"name": "society_subarea", "type": "STRING"},
                                  {"name": "society_latitude", "type": "STRING"},
                                  {"name": "society_location_type", "type": "STRING"},
                                  {"name": "society_type_quality", "type": "STRING"},
                                  {"name": "society_type_quantity", "type": "STRING"},
                                  {"name": "flat_count", "type": "STRING"},
                                  {"name": "flat_avg_rental_persqft", "type": "STRING"},
                                  {"name": "flat_sale_cost_persqft", "type": "STRING"},
                                  {"name": "tower_count", "type": "INT"},
                                  {"name": "payment_details_available", "type": "BOOLEAN"},
                                  {"name": "age_of_society", "type": "INT"},
                                  {"name": "total_tenant_flat_count", "type": "INT"},
                                  {"name": "landmark", "type": "STRING"},
                                  {"name": "name_for_payment", "type": "STRING"},
                                  {"name": "bank_name", "type": "STRING  "},
                                  {"name": "ifsc_code", "type": "STRING"},
                                  {"name": "account_no", "type": "STRING"},
                              {"name": "representative", "type": "STRING"}],
            "organisation_id": "MAC1421",

        }).save()
        new_supplier_type_id = new_supplier_type_for_society._id
        supplier_list = []
        counter = 0
        for society in society_list:
            if society['society_name']:
                name = society['society_name']
                new_supplier_type_id = new_supplier_type_id
                supplier_attributes = [
                                  {"name": "supplier_id", "type": "STRING", "value": society['supplier_id']},
                                  {"name": "name", "type": "STRING", "value": society['society_name']},
                                  {"name": "society_address1", "type": "STRING", "value": society['society_address1']},
                                  {"name": "society_address2", "type": "STRING", "value": society['society_address2']},
                                  {"name": "society_zip", "type": "STRING", "value": society['society_zip']},
                                  {"name": "society_name", "type": "STRING", "value": society['society_name']},
                                  {"name": "society_city", "type": "STRING", "value": society['society_city']},
                                  {"name": "society_state", "type": "STRING", "value": society['society_state']},
                                  {"name": "society_longitude", "type": "STRING", "value": society['society_longitude']},
                                  {"name": "society_locality", "type": "STRING", "value": society['society_locality']},
                                  {"name": "society_subarea", "type": "STRING", "value": society['society_subarea']},
                                  {"name": "society_latitude", "type": "STRING", "value": society['society_latitude']},
                                  {"name": "society_location_type", "type": "STRING", "value": society['society_location_type']},
                                  {"name": "society_type_quality", "type": "STRING", "value": society['society_type_quality']},
                                  {"name": "society_type_quantity", "type": "STRING", "value": society['society_type_quantity']},
                                  {"name": "flat_count", "type": "STRING", "value": society['flat_count']},
                                  {"name": "flat_avg_rental_persqft", "type": "STRING", "value": society['flat_avg_rental_persqft']},
                                  {"name": "flat_sale_cost_persqft", "type": "STRING", "value": society['flat_sale_cost_persqft']},
                                  {"name": "tower_count", "type": "INT", "value": society['tower_count']},
                                  {"name": "payment_details_available", "type": "BOOLEAN", "value": society['payment_details_available']},
                                  {"name": "age_of_society", "type": "INT", "value": society['age_of_society']},
                                  {"name": "total_tenant_flat_count", "type": "INT", "value": society['total_tenant_flat_count']},
                                  {"name": "landmark", "type": "STRING", "value": society['landmark']},
                                  {"name": "name_for_payment", "type": "STRING", "value": society['name_for_payment']},
                                  {"name": "bank_name", "type": "STRING", "value": society['bank_name']},
                                  {"name": "ifsc_code", "type": "STRING", "value": society['ifsc_code']},
                                  {"name": "account_no", "type": "STRING", "value": society['account_no']},
                                  {"name": "representative", "type": "STRING", "value": society['representative']}
                                ],

                organisation_id = "MAC1421"
                dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes[0],
                                          "organisation_id": organisation_id,
                                          "supplier_type_id": new_supplier_type_id,
                                          "old_supplier_id": society['supplier_id']}
                supplier_dict = dict_of_req_attributes
                supplier_dict["created_at"] = datetime.now()
                supplier_list.append(SupplySupplier(**supplier_dict))
                counter = counter + 1
                if counter % 500 == 0:
                    SupplySupplier.objects.bulk_create(supplier_list)
                    supplier_list = []
        if len(supplier_list) > 0:
            SupplySupplier.objects.bulk_create(supplier_list)
        return handle_response('', data={"success": True}, success=True)


class ShortlistedSpacesTransfer(APIView):
    @staticmethod
    def get(request):
        shortlisted_spaces = ShortlistedSpaces.objects.all()
        serializer = ShortlistedSpacesSerializer(shortlisted_spaces, many=True)
        shortlisted_spaces_list = serializer.data
        base_supplier_type = BaseSupplySupplierType.objects.raw({'name': 'Base Society'})[0]
        supplier_type = SupplySupplierType.objects.raw({'name': 'Base Society'})[0]
        booking_attributes_list = [

                                {"name": "payment_method", "type": "DROPDOWN", "options": ["NEFT", "CASH", "ONLINE"]},
                                {"name": "payment_status", "type": "DROPDOWN", "options": ["Not Initiated", "Pending", "Cheque Released",
                                                                                           "Paid", "Rejected"]},
                                {"name": "status", "type":"DROPDOWN", "options": ["BUFFER", "REMOVED", "FINALIZED"]},
                                {"name": "total_negotiated_price", "type":"FLOAT"},
                                {"name": "booking_status", "type": "DROPDOWN", "options": ["Undecided",
                                    "Decision Pending", "Conformed Booking", "Tentative Booking", "Phone Booked", "Visit Booked",
                                    "Rejected", "Send Email", "Visit Required", "Call Required"]},

                                {"name": "is_completed", "type": "BOOLEAN"},
                                {"name": "transaction_or_check_number", "type": "STRING"},
                                {"name": "phase_no", "type": "INT"},
                                {"name": "freebies", "type": "MULTISELECT", "options": ["Whatsapp Group","Email Group",
                                                                                     "Building ERP", " Door to Door"]},
                                {"name": "stall_locations", "type": "MULTISELECT", "options": ["Nea Entry Gate","Near Exit Gate",
                                        "In Front Of Tower", "Near Garden", "Near Play Area", "Near Club House",
                                        "Near Swimming Pool", "Near Parking Area", "Near Shopping Area"]},
                                {"name": "cost_per_flat", "type": "FLOAT"},
                                {"name": "booking_priority", "type": "DROPDOWN", "options": ["Very High", "High"]},
                                {"name": "sunboard_location", "type": "MULTISELECT", "options": ["Nea Entry Gate","Near Exit Gate",
                                        "In Front Of Tower", "Near Garden", "Near Play Area", "Near Club House",
                                        "Near Swimming Pool", "Near Parking Area", "Near Shopping Area"]},

                                ]
        new_base_booking_template = BaseBookingTemplate(**
        {
            "name": "Society BaseBooking",
            "booking_attributes": booking_attributes_list,
            "base_supplier_type_id": base_supplier_type._id,
            "supplier_attributes": base_supplier_type.supplier_attributes,
            "organisation_id": "MAC1421"
         }).save()
        new_base_booking_template_id = new_base_booking_template._id
        new_booking_template = BookingTemplate(**
        {
            "name":"Society Booking",
            "booking_attributes": booking_attributes_list,
            "supplier_type_id": supplier_type._id,
            "base_booking_template_id": new_base_booking_template_id,
            "supplier_attributes": supplier_type.supplier_attributes,
            "organisation_id": "MAC1421"
        }).save()
        new_booking_template_id = new_booking_template._id
        booking_list = []
        counter = 0
        for booking in shortlisted_spaces_list:
            data = {}
            data['booking_template_id'] = str(new_booking_template_id)
            data['campaign_id'] = booking['proposal']
            data['user_id'] = booking['user']
            data['center_id'] = booking['center']
            data['supplier_id_old'] = booking['object_id']
            temp_data = SupplySupplier.objects.raw({'old_supplier_id':booking['object_id']})
            if  temp_data.count() > 0:
                data['supplier_id'] = temp_data[0]._id
            else:
                continue
            for item in booking_attributes_list:
                item['value'] = booking[item['name']]
            data['booking_attributes'] = booking_attributes_list
            booking_list.append(BookingData(**data))
            counter = counter + 1
            if counter % 1000 == 0:
                BookingData.objects.bulk_create(booking_list)
                booking_list = []
        if len(booking_list) > 0:
            BookingData.objects.bulk_create(booking_list)
        return handle_response('', data={"success": True}, success=True)

class SupplierInventoryTransfer(APIView):
    @staticmethod
    def get(request):
        supplier_inventories = ShortlistedInventoryPricingDetails.objects.all()
        for inventory in supplier_inventories:
            data = {}
            if SupplySupplier.objects.raw({'old_supplier_id': inventory.shortlisted_spaces.object_id}).count() > 0:
                data['supplier_id'] = SupplySupplier.objects.raw({'old_supplier_id': inventory.shortlisted_spaces.object_id})[0]._id
            else:
                continue
            data['campaign_id'] = inventory.shortlisted_spaces.proposal.proposal_id
            data['inventory_name'] = inventory.ad_inventory_type.adinventory_name
            data['organisation_id'] = inventory.shortlisted_spaces.proposal.account.organisation.organisation_id
            data['supplier_id_old'] = inventory.shortlisted_spaces.object_id
            data['comments'] = []
            data['inventory_images'] = []
            data['created_by'] = inventory.user
            data["created_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            data["inventory_id_old"] = inventory.id

            BookingInventory(**data).save()

        return handle_response('', data={"success": True}, success=True)

class InventoryActivityImageTransfer(APIView):
    def get(self, request):
        dynamic_inventory = BookingInventory.objects.raw({})
        dynamic_inventory_ids_map = {inv.inventory_id_old: inv for inv in dynamic_inventory}

        dynamic_supplier = SupplySupplier.objects.raw({})
        dynamic_supplier_ids_map = {supplier.old_supplier_id:supplier for supplier in dynamic_supplier}

        image_objects = InventoryActivityImage.objects.select_related('inventory_activity_assignment',
                                                      'inventory_activity_assignment__inventory_activity',
                                                      'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details',
                                                      'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces',
                                                      'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal')
        result = {}
        for item in image_objects:
            try:
                if item and str(item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.id) in dynamic_inventory_ids_map:
                    if item.inventory_activity_assignment not in result:

                        result[item.inventory_activity_assignment] = {
                            'booking_inventory_id': str(dynamic_inventory_ids_map[str(item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.id)]._id),
                            'supplier_id': str(dynamic_supplier_ids_map[item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.shortlisted_spaces.object_id]._id),
                            'inventory_name': item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.ad_inventory_type.adinventory_name,
                            'comments': [],
                            'campaign_id': item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.shortlisted_spaces.proposal.proposal_id,
                            'organisation_id': 'MAC1421',
                            'inventory_images': [],
                            'activity_type': item.inventory_activity_assignment.inventory_activity.activity_type,
                            'activity_date': item.inventory_activity_assignment.activity_date,
                            'assigned_to_id': item.inventory_activity_assignment.assigned_to.id
                        }
                    result[item.inventory_activity_assignment]['inventory_images'].append({
                        'image_path': item.image_path,
                        'latitude': item.latitude,
                        'longitude': item.longitude,
                        'comment': item.comment,
                        'actual_activity_date': item.actual_activity_date,
                        'activity_by': item.activity_by.id
                    })
            except Exception as e:
                continue
        for item in result.values():
            BookingInventoryActivity(**item).save()
        return handle_response('', data={}, success=True)

def create_auto_complete_supplier_data(supplier_list=None):

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for supplier in supplier_list:
        supplier_name = supplier.name.lower()
        supplier_id = str(supplier._id)
        line = supplier_name
        '''+ '||' + str(supplier_id)'''
        n = line.strip()
        for l in range(1, len(n)):
            prefix = n[0:l]
            r.zadd('supplier_data', 0, prefix)
        r.zadd('supplier_data', 0, n + "*" + str(supplier_id))
    return handle_response('', data={}, success=True)

class AutoCompleteSupplierDataCreate(APIView):
    @staticmethod
    def get(request):
        suppliers = SupplySupplier.objects.all()
        response = create_auto_complete_supplier_data(suppliers)
        if response.data['status']:
            return handle_response('', data={}, success=True)
        return handle_response('', data={}, success=False)

class SupplierAutoComplete(APIView):
    @staticmethod
    def get(request):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        query = request.query_params.get('query','')
        prefix = query.lower()

        results = []
        rangelen = 50  # This is not random, try to get replies < MTU size
        start = r.zrank('supplier_data', prefix)
        print(prefix, start)

        if start is None:
            # print "start is none"
            return handle_response('', data=[], success=True)
        redis_data = r.zrange('supplier_data', start, start + rangelen - 1)
        redis_data = [data.decode('UTF-8') for data in redis_data]
        print(redis_data)
        try:
            k = r.zrange('supplier_data', start + rangelen - 1, start + rangelen - 1)
            print("hi", k)
            while k[0].startswith(prefix):
                start = start + 50
                redis_data = r.zrange('supplier_data', start, start + rangelen - 1)
                print(redis_data)
                redis_data.extend(redis_data)
                k = r.zrange('supplier_data', start + rangelen -
                             1, start + rangelen - 1)
        except:

            for i in redis_data:

                if i.startswith(prefix):

                    if '*' in i:
                        i_arr = i.split('*')
                        i_obj = {'name': i_arr[0], 'id': i_arr[1]}
                        results.append(i_obj)

            return handle_response('', data=results, success=True)