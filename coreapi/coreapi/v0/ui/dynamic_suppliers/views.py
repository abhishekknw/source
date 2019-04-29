from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import BaseSupplySupplierType, SupplySupplierType, SupplySupplier
from bson.objectid import ObjectId
from datetime import datetime
from .utils import validate_supplier_type_data, validate_with_supplier_type
from v0.ui.supplier.models import (SupplierTypeSociety)
from v0.ui.proposal.models import (ShortlistedSpaces)
from v0.ui.inventory.serializers import (ShortlistedSpacesSerializer)
from v0.ui.dynamic_booking.models import BookingData
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2


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
                                  {"name":"society_name","type": "STRING"},
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
                                  {"name": "society_name", "type": "STRING"},
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
            "organisation_id": "MAC1421"
        }).save()
        new_supplier_type_id = new_supplier_type_for_society._id
        for society in society_list:
            name = 'Society'
            new_supplier_type_id = new_supplier_type_id
            supplier_attributes = society
            organisation_id = "MAC1421"
            dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes,
                                      "organisation_id": organisation_id,
                                      "supplier_type_id": new_supplier_type_id}
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
        ## STEPS
        ## STEP 1 create base booking template
        ## STEP 2 create booking template
        ## STEP 3 Loop over shortlisted_spaces_list and get new supplier_id from shorlisted_space's object_id
        ## STEP 4 create the object for booking_data (which was shortlisted_spaces in old version) and save it
        return handle_response('', data={"success": True}, success=True)
