from rest_framework.views import APIView
from v0.ui.utils import handle_response, create_validation_msg
from models import BaseSupplyEntityType
from bson.objectid import ObjectId
from datetime import datetime
from utils import validate_entity_type_data


class BaseEntityType(APIView):

    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else False
        entity_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else False
        dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        entity_type_dict = dict_of_req_attributes
        entity_type_dict["created_at"] = datetime.now()
        is_valid_adv, validation_msg_dict_adv = validate_entity_type_data(entity_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        BaseSupplyEntityType(**entity_type_dict).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        all_base_supply_entity_type = BaseSupplyEntityType.objects.all()
        all_base_supply_entity_type_dict = {}
        for base_supply_entity_type in all_base_supply_entity_type:
            all_base_supply_entity_type_dict[str(base_supply_entity_type._id)] = {
                "id": str(base_supply_entity_type._id),
                "name": base_supply_entity_type.name,
                "entity_attributes": base_supply_entity_type.entity_attributes
            }
        return handle_response('', data=all_base_supply_entity_type_dict, success=True)


class BaseEntityTypeById(APIView):
    @staticmethod
    def get(request, base_entity_type_id):
        base_supply_entity_type = BaseSupplyEntityType.objects.raw({'_id':ObjectId(base_entity_type_id)})[0]
        base_supply_entity_type = {
            "id": str(base_supply_entity_type._id),
            "name": base_supply_entity_type.name,
            "entity_attributes": base_supply_entity_type.entity_attributes
        }
        return handle_response('', data=base_supply_entity_type, success=True)

    @staticmethod
    def put(request, base_entity_type_id):
        new_name = request.data['name'] if 'name' in request.data else None
        new_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else None
        dict_of_req_attributes = {"name": new_name, "entity_attributes": new_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        base_entity_type_dict = dict_of_req_attributes
        base_entity_type_dict["updated_at"] = datetime.now()
        is_valid_adv, validation_msg_dict_adv = validate_entity_type_data(base_entity_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        BaseSupplyEntityType.objects.raw({'_id': ObjectId(base_entity_type_id)}).update({"$set": base_entity_type_dict})
        return handle_response('', data="success", success=True)


    @staticmethod
    def delete(request, base_entity_type_id):
        exist_entity_query = BaseSupplyEntityType.objects.raw({'_id': ObjectId(base_entity_type_id)})[0]
        exist_entity_query.delete()
        return handle_response('', data="success", success=True)
