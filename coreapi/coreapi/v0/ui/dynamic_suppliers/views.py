from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import BaseSupplySupplierType, SupplySupplierType, SupplySupplier
from bson.objectid import ObjectId
from datetime import datetime
from .utils import validate_supplier_type_data, validate_with_supplier_type
from v0.ui.supplier.models import (SupplierTypeSociety)
from v0.ui.proposal.models import (ShortlistedSpaces)
from v0.ui.inventory.serializers import (ShortlistedSpacesSerializer, ShortlistedInventoryPricingDetailsSerializer)
from v0.ui.dynamic_booking.models import BookingData
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2
from v0.ui.dynamic_booking.models import BaseBookingTemplate, BookingTemplate, BookingData, BookingInventory
from v0.ui.finances.models import ShortlistedInventoryPricingDetails


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
                "supplier_attributes": supply_supplier_type.supplier_attributes
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
            "supplier_attributes": supply_supplier_type.supplier_attributes
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
        is_valid_adv, validation_msg_dict_adv = validate_supplier_type_data(supplier_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
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
        (is_valid_adv, validation_msg_dict_adv) = validate_with_supplier_type(supplier_dict,supplier_type_id)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplySupplier(**supplier_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_supply_supplier = SupplySupplier.objects.all()
        all_supply_supplier_dict = {}
        for supply_supplier in all_supply_supplier:
            all_supply_supplier_dict[str(supply_supplier._id)] = {
                "id": str(supply_supplier._id),
                "supplier_type_id": str(supply_supplier.supplier_type_id),
                "name": supply_supplier.name,
                "supplier_attributes": supply_supplier.supplier_attributes,
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
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "supplier_type_id": supplier_type_id, "is_custom": is_custom,
                                  "supplier_attributes": supplier_attributes, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_dict = dict_of_req_attributes
        supplier_dict['updated_at'] = datetime.now()
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
                SupplySupplier(**supplier_dict).save()
        return handle_response('', data={"success": True}, success=True)


class ShortlistedSpacesTransfer(APIView):
    @staticmethod
    def get(request):
        shortlisted_spaces = ShortlistedSpaces.objects.all()
        serializer = ShortlistedSpacesSerializer(shortlisted_spaces, many=True)
        shortlisted_spaces_list = serializer.data
        print(shortlisted_spaces_list[0])
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
            "base_supplier_type_id": "5c66829e2f2bc6117aac7c75"
         }).save()
        new_base_booking_template_id = new_base_booking_template._id
        new_booking_template = BookingTemplate(**
        {
            "name":"Society Booking",
            "booking_attributes": booking_attributes_list,
            "supplier_type_id": "5ca4ad779cb7fc6da6d92797",
            "base_booking_template_id": new_base_booking_template_id
        }).save()
        new_booking_template_id = new_booking_template._id
        for booking in shortlisted_spaces_list:
            data = {}
            data['booking_template_id'] = new_booking_template_id,
            data['campaign_id'] = booking['proposal']
            data['user_id'] = booking['user']
            data['center_id'] = booking['center']
            data['supplier_id_old'] = booking['object_id']
            if SupplySupplier.objects.raw({'old_supplier_id':booking['object_id']}).count() > 0:
                data['supplier_id'] = SupplySupplier.objects.raw({'old_supplier_id':booking['object_id']})[0]._id
            else:
                continue
            for item in booking_attributes_list:
                item['value'] = booking[item['name']]
            data['booking_attributes'] = booking_attributes_list
            BookingData(**data).save()
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

            BookingInventory(**data).save()

        return handle_response('', data={"success": True}, success=True)