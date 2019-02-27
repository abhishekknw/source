from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import SupplyEntityType, SupplyEntity
from bson.objectid import ObjectId
from datetime import datetime
from .utils import validate_entity_type_data, validate_with_entity_type
from v0.ui.supplier.models import (SupplierTypeSociety)
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2


class EntityType(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else False
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        entity_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else False
        organisation_id = get_user_organisation_id(request.user)
        base_entity_type_id = request.data['base_entity_type_id'] if 'base_entity_type_id' in request.data else False
        dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes,
                                  "organisation_id": organisation_id, "base_entity_type_id": base_entity_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        entity_type_dict = dict_of_req_attributes
        entity_type_dict["is_global"] = is_global
        entity_type_dict["created_at"] = datetime.now()
        is_valid_adv, validation_msg_dict_adv = validate_entity_type_data(entity_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplyEntityType(**entity_type_dict).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        all_supply_entity_type = SupplyEntityType.objects.all()
        all_supply_entity_type_dict = {}
        for supply_entity_type in all_supply_entity_type:
            all_supply_entity_type_dict[str(supply_entity_type._id)] = {
                "id": str(supply_entity_type._id),
                "base_entity_type_id": str(supply_entity_type.base_entity_type_id),
                "name": supply_entity_type.name,
                "entity_attributes": supply_entity_type.entity_attributes
            }
        return handle_response('', data=all_supply_entity_type_dict, success=True)


class EntityTypeById(APIView):
    @staticmethod
    def get(request, entity_type_id):
        supply_entity_type = SupplyEntityType.objects.raw({'_id':ObjectId(entity_type_id)})[0]
        supply_entity_type = {
            "id": str(supply_entity_type._id),
            "base_entity_type_id": str(supply_entity_type.base_entity_type_id),
            "name": supply_entity_type.name,
            "entity_attributes": supply_entity_type.entity_attributes
        }
        return handle_response('', data=supply_entity_type, success=True)


    @staticmethod
    def put(request, entity_type_id):
        new_name = request.data['name'] if 'name' in request.data else None
        new_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        base_entity_type_id = request.data['base_entity_type_id'] if 'base_entity_type_id' in request.data else False
        dict_of_req_attributes = {"name": new_name, "entity_attributes": new_attributes,
                                  "base_entity_type_id": base_entity_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        entity_type_dict = dict_of_req_attributes
        entity_type_dict["is_global"] = is_global
        entity_type_dict["updated_at"] = datetime.now()
        is_valid_adv, validation_msg_dict_adv = validate_entity_type_data(entity_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplyEntityType.objects.raw({'_id': ObjectId(entity_type_id)}).update({"$set": entity_type_dict})
        return handle_response('', data="success", success=True)


    @staticmethod
    def delete(request, entity_type_id):
        exist_entity_query = SupplyEntityType.objects.raw({'_id': ObjectId(entity_type_id)})[0]
        exist_entity_query.delete()
        return handle_response('', data="success", success=True)


class Entity(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        entity_type_id = request.data['entity_type_id'] if 'entity_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        entity_attributes = request.data['entity_attributes']
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "entity_type_id": entity_type_id, "is_custom": is_custom,
                                  "entity_attributes": entity_attributes, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        entity_dict = dict_of_req_attributes
        entity_dict['created_by'] = request.user.id
        entity_dict['created_at'] = datetime.now()
        (is_valid_adv, validation_msg_dict_adv) = validate_with_entity_type(entity_dict,entity_type_id)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplyEntity(**entity_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_supply_entity = SupplyEntity.objects.all()
        all_supply_entity_dict = {}
        for supply_entity in all_supply_entity:
            all_supply_entity_dict[str(supply_entity._id)] = {
                "id": str(supply_entity._id),
                "entity_type_id": str(supply_entity.entity_type_id),
                "name": supply_entity.name,
                "entity_attributes": supply_entity.entity_attributes,
                "is_custom": supply_entity.is_custom,
                "organisation_id": supply_entity.organisation_id,
                "created_by": supply_entity.created_by,
                "created_at": supply_entity.created_at,
            }
        return handle_response('', data=all_supply_entity_dict, success=True)


class EntityById(APIView):
    @staticmethod
    def get(request, entity_id):
        supply_entity = SupplyEntity.objects.raw({'_id':ObjectId(entity_id)})[0]
        supply_entity = {
            "id": str(supply_entity._id),
            "entity_type_id": str(supply_entity.entity_type_id),
            "name": supply_entity.name,
            "entity_attributes": supply_entity.entity_attributes,
            "is_custom": supply_entity.is_custom,
            "organisation_id": supply_entity.organisation_id,
            "created_by": supply_entity.created_by,
            "created_at": supply_entity.created_at,
        }
        return handle_response('', data=supply_entity, success=True)

    @staticmethod
    def put(request, entity_id):
        name = request.data['name'] if 'name' in request.data else None
        entity_type_id = request.data['entity_type_id'] if 'entity_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        entity_attributes = request.data['entity_attributes']
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "entity_type_id": entity_type_id, "is_custom": is_custom,
                                  "entity_attributes": entity_attributes, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        entity_dict = dict_of_req_attributes
        entity_dict['updated_at'] = datetime.now()
        (is_valid_adv, validation_msg_dict_adv) = validate_with_entity_type(entity_dict, entity_type_id)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplyEntity.objects.raw({'_id': ObjectId(entity_id)}).update({"$set": entity_dict})
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, entity_id):
        exist_entity_query = SupplyEntity.objects.raw({'_id': ObjectId(entity_id)})[0]
        exist_entity_query.delete()
        return handle_response('', data="success", success=True)


class EntityTypeSociety(APIView):
    @staticmethod
    def get(request):
        supplier_objects = SupplierTypeSociety.objects.all()
        print(supplier_objects)
        serializer = SupplierTypeSocietySerializer(supplier_objects, many=True)
        print(serializer.data)
        society_list = serializer.data
        for society in society_list:
            name = 'Society'
            is_global = True
            entity_attributes = society
            organisation_id = "MAC1421"
            dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes,
                                  "organisation_id": organisation_id}
            entity_type_dict = dict_of_req_attributes
            entity_type_dict["is_global"] = is_global
            entity_type_dict["created_at"] = datetime.now()
            SupplyEntityType(**entity_type_dict).save()
        return handle_response('', data={"success": True}, success=True)
