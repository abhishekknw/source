from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from models import BaseInventory, Inventory
from bson.objectid import ObjectId
from datetime import datetime
from validate_email import validate_email


class BaseInventoryAPI(APIView):

    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        base_attributes = request.data['base_attributes'] if 'base_attributes' in request.data else None
        inventory_type = request.data['inventory_type'] if 'inventory_type' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "base_attributes": base_attributes,
                                  "organisation_id": organisation_id, "inventory_type": inventory_type}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        entity_type_dict = dict_of_req_attributes
        entity_type_dict["is_global"] = is_global
        entity_type_dict["created_at"] = datetime.now()
        BaseInventory(**entity_type_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_base_inventory = BaseInventory.objects.all()
        all_base_inventory_dict = {}
        for base_inventory in all_base_inventory:
            all_base_inventory_dict[str(base_inventory._id)] = {
                "_id": str(base_inventory._id),
                "name": base_inventory.name,
                "base_attributes": base_inventory.base_attributes
            }
        return handle_response('', data=all_base_inventory_dict, success=True)