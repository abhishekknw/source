from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg, validate_attributes
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
        (is_valid_attributes, validation_msg_dict_attributes) = validate_attributes(inventory_attributes)
        if not is_valid_attributes:
            return handle_response('', data=validation_msg_dict_attributes, success=False)
        base_inventory_dict = dict_of_req_attributes
        base_inventory_dict["is_global"] = is_global
        base_inventory_dict["created_at"] = datetime.now()
        BaseInventory(**base_inventory_dict).save()
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


class BaseInventoryAPIById(APIView):
    @staticmethod
    def get(request, base_inventory_id):
        base_inventory = BaseInventory.objects.raw({'_id': ObjectId(base_inventory_id)})[0]
        base_inventory = {
            "_id": str(base_inventory._id),
            "name": base_inventory.name,
            "entity_attributes": base_inventory.base_attributes
        }
        return handle_response('', data=base_inventory, success=True)


    @staticmethod
    def put(request, base_inventory_id):
        name = request.data['name'] if 'name' in request.data else None
        base_attributes = request.data['base_attributes'] if 'base_attributes' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        inventory_type = request.data['inventory_type'] if 'inventory_type' in request.data else None
        dict_of_req_attributes = {"name": name, "base_attributes": base_attributes, "inventory_type":inventory_type}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        (is_valid_attributes, validation_msg_dict_attributes) = validate_attributes(inventory_attributes)
        if not is_valid_attributes:
            return handle_response('', data=validation_msg_dict_attributes, success=False)
        base_inventory_dict = dict_of_req_attributes
        base_inventory_dict["is_global"] = is_global
        base_inventory_dict["updated_at"] = datetime.now()
        BaseInventory.objects.raw({'_id': ObjectId(base_inventory_id)}).update({"$set": base_inventory_dict})
        return handle_response('', data="success", success=True)


class InventoryAPI(APIView):

    @staticmethod
    def post(request):

        # all_fields = ['name', 'is_global', 'base_inventory', 'inventory_attributes', 'organisation_id']
        #
        # for curr_field in all_fields:

        name = request.data['name'] if 'name' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        base_inventory = request.data['base_inventory'] if 'base_inventory' in request.data else None
        inventory_attributes = request.data['inventory_attributes'] if 'inventory_attributes' in request.data else None
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "base_inventory": base_inventory,
                                  "organisation_id": organisation_id, "inventory_attributes": inventory_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        (is_valid_attributes, validation_msg_dict_attributes) = validate_attributes(inventory_attributes)
        if not is_valid_attributes:
            return handle_response('', data=validation_msg_dict_attributes, success=False)
        inventory_dict = dict_of_req_attributes
        inventory_dict["is_global"] = is_global
        inventory_dict["created_at"] = datetime.now()
        Inventory(**inventory_dict).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        all_inventory = Inventory.objects.all()
        all_inventory_dict = {}
        for inventory in all_inventory:
            all_inventory_dict[str(inventory._id)] = {
                "_id": str(inventory._id),
                "name": inventory.name,
                "base_inventory": inventory.base_inventory,
                "inventory_attributes": inventory.inventory_attributes
            }
        return handle_response('', data=all_inventory_dict, success=True)


class InventoryAPIById(APIView):
    @staticmethod
    def get(request, inventory_id):
        inventory_db = Inventory.objects.raw({'_id': ObjectId(inventory_id)})[0]
        inventory = {
            "_id": str(inventory_db._id),
            "name": inventory_db.name,
            "base_inventory": inventory_db.base_inventory,
            "inventory_attributes": inventory_db.inventory_attributes
        }
        return handle_response('', data=inventory, success=True)

    @staticmethod
    def put(request, inventory_id):
        name = request.data['name'] if 'name' in request.data else None
        base_inventory = request.data['base_inventory'] if 'base_inventory' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        inventory_attributes = request.data['inventory_attributes'] if 'inventory_attributes' in request.data else None
        dict_of_req_attributes = {"name": name, "base_inventory": base_inventory,
                                  "inventory_attributes": inventory_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        (is_valid_attributes, validation_msg_dict_attributes) = validate_attributes(inventory_attributes)
        if not is_valid_attributes:
            return handle_response('', data=validation_msg_dict_attributes, success=False)
        inventory_dict = dict_of_req_attributes
        inventory_dict["is_global"] = is_global
        inventory_dict["updated_at"] = datetime.now()
        Inventory.objects.raw({'_id': ObjectId(inventory_id)}).update({"$set": inventory_dict})
        return handle_response('', data="success", success=True)

    @staticmethod
    def delete(request, inventory_id):
        if not inventory_id:
            return handle_response('', data="Inventory Id Not Provided", success=False)
        inventory_query = Inventory.objects.raw({'_id': ObjectId(inventory_id)})
        inventory_query.delete()
        return handle_response('', data="success", success=True)