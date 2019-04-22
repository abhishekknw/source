from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, create_validation_msg
from .models import BaseSupplySupplierType
from bson.objectid import ObjectId
from datetime import datetime
from .utils import validate_supplier_type_data


class BaseSupplierType(APIView):

    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else False
        supplier_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else False
        dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_type_dict = dict_of_req_attributes
        supplier_type_dict["created_at"] = datetime.now()
        # is_valid_adv, validation_msg_dict_adv = validate_supplier_type_data(supplier_type_dict)
        # if not is_valid_adv:
        #     return handle_response('', data=validation_msg_dict_adv, success=False)
        BaseSupplySupplierType(**supplier_type_dict).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        all_base_supply_supplier_type = BaseSupplySupplierType.objects.all()
        all_base_supply_supplier_type_dict = {}
        for base_supply_supplier_type in all_base_supply_supplier_type:
            all_base_supply_supplier_type_dict[str(base_supply_supplier_type._id)] = {
                "id": str(base_supply_supplier_type._id),
                "name": base_supply_supplier_type.name,
                "supplier_attributes": base_supply_supplier_type.supplier_attributes
            }
        return handle_response('', data=all_base_supply_supplier_type_dict, success=True)


class BaseSupplierTypeById(APIView):
    @staticmethod
    def get(request, base_supplier_type_id):
        base_supply_supplier_type = BaseSupplySupplierType.objects.raw({'_id':ObjectId(base_supplier_type_id)})[0]
        base_supply_supplier_type = {
            "id": str(base_supply_supplier_type._id),
            "name": base_supply_supplier_type.name,
            "supplier_attributes": base_supply_supplier_type.supplier_attributes
        }
        return handle_response('', data=base_supply_supplier_type, success=True)

    @staticmethod
    def put(request, base_supplier_type_id):
        new_name = request.data['name'] if 'name' in request.data else None
        new_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else None
        dict_of_req_attributes = {"name": new_name, "supplier_attributes": new_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        base_supplier_type_dict = dict_of_req_attributes
        base_supplier_type_dict["updated_at"] = datetime.now()
        # is_valid_adv, validation_msg_dict_adv = validate_supplier_type_data(base_supplier_type_dict)
        # if not is_valid_adv:
        #     return handle_response('', data=validation_msg_dict_adv, success=False)
        BaseSupplySupplierType.objects.raw({'_id': ObjectId(base_supplier_type_id)}).update({"$set": base_supplier_type_dict})
        return handle_response('', data="success", success=True)


    @staticmethod
    def delete(request, base_supplier_type_id):
        exist_supplier_query = BaseSupplySupplierType.objects.raw({'_id': ObjectId(base_supplier_type_id)})[0]
        exist_supplier_query.delete()
        return handle_response('', data="success", success=True)
