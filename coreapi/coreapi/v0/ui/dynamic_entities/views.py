from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from models import SupplyEntityType, SupplyEntity
from bson.objectid import ObjectId
from datetime import datetime
from validate_email import validate_email


def validate_entity_type_data(entity_type_dict):
    possible_attribute_types = ['FLOAT', 'INT', 'STRING', 'BOOLEAN', 'EMAIL', 'PASSWORD', 'PHONE', 'DROPDOWN', 'RADIO',
                                'CHECKBOX', 'TEXTAREA', 'DATE', 'DATETIME', 'INVENTORYLIST']
    validation_msg_dict = {'repeating_name_field': [], "type_mismatch": []}
    is_valid = True
    entity_type_attributes = entity_type_dict["entity_attributes"]
    all_attribute_names = []
    for single_attribute in entity_type_attributes:
        if single_attribute['name'] in all_attribute_names:
            is_valid = False
            validation_msg_dict['repeating_name_field'].append(single_attribute['name'])
        if single_attribute['type'] not in possible_attribute_types:
            is_valid = False
            validation_msg_dict['type_mismatch'].append(single_attribute['type'])
        all_attribute_names.append(single_attribute['name'])
    return is_valid, validation_msg_dict


class EntityType(APIView):

    @staticmethod
    def post(request):
        name = request.data['name']
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        entity_attributes = request.data['entity_attributes']
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes,
                                  "organisation_id": organisation_id}
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
                "_id": str(supply_entity_type._id),
                "name": supply_entity_type.name,
                "entity_attributes": supply_entity_type.entity_attributes
            }
        return handle_response('', data=all_supply_entity_type_dict, success=True)


class EntityTypeById(APIView):
    @staticmethod
    def get(request, entity_type_id):
        supply_entity_type = SupplyEntityType.objects.raw({'_id':ObjectId(entity_type_id)})[0]
        supply_entity_type = {
            "_id": str(supply_entity_type._id),
            "name": supply_entity_type.name,
            "entity_attributes": supply_entity_type.entity_attributes
        }
        return handle_response('', data=supply_entity_type, success=True)


    @staticmethod
    def put(request, entity_type_id):
        new_name = request.data['name'] if 'name' in request.data else None
        new_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        dict_of_req_attributes = {"name": new_name, "entity_attributes": new_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        entity_type_dict = dict_of_req_attributes
        entity_type_dict["is_global"] = is_global
        entity_type_dict["updated_at"] = datetime.now()
        is_valid_adv, validation_msg_dict_adv = validate_entity_type_data(entity_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplyEntity.objects.raw({'_id': ObjectId(entity_type_id)}).update({"$set": entity_type_dict})
        return handle_response('', data="success", success=True)


    @staticmethod
    def delete(request, entity_type_id):
        exist_entity_query = SupplyEntityType.objects.raw({'_id': ObjectId(entity_type_id)})[0]
        exist_entity_query.delete()
        return handle_response('', data="success", success=True)


def validate_attribute_with_type(entity_type_attribute_dict, attribute_value):
    attribute_is_valid = True
    attribute_type = entity_type_attribute_dict['type']
    if attribute_type in ['DROPDOWN', 'CHECKBOX', 'RADIO']:
        attribute_options = entity_type_attribute_dict['options'] if 'options' in entity_type_attribute_dict else None
        if not attribute_options:
            return False
        if attribute_value not in attribute_options:
            return False
    if attribute_type == 'FLOAT' and (isinstance(attribute_value,float) or isinstance(attribute_value,int)) is False:
        return False
    if attribute_type == 'INT' and isinstance(attribute_value,int) is False:
        return False
    if attribute_type == 'STRING' and isinstance(attribute_value,basestring) is False:
        return False
    if attribute_type == 'BOOLEAN' and isinstance(attribute_value,bool) is False:
        return False
    if attribute_type == 'EMAIL':
        return validate_email(attribute_value)
    if attribute_type == 'PASSWORD' and isinstance(attribute_value,basestring) is False:
        return False
    if attribute_type == 'TEXTAREA' and isinstance(attribute_value,basestring) is False:
        return False
    if attribute_type == 'DATE' and isinstance(attribute_value,datetime.date) is False:
        return False
    if attribute_type == 'DATETIME' and isinstance(attribute_value,datetime) is False:
        return False
    return attribute_is_valid


def validate_with_entity_type(entity_dict,entity_type_id):
    entity_type = list(SupplyEntityType.objects.raw({'_id': ObjectId(entity_type_id)}))
    validation_msg_dict = {'missing_data': [], "data_mismatch": []}
    is_valid = True
    if len(entity_type) == 0:
        validation_msg_dict['data_mismatch'].append("entity_type_id")
        return (False, validation_msg_dict)
    entity_type = entity_type[0]
    entity_type_attribute_dict = {single_attribute["name"]: single_attribute for single_attribute in entity_type.entity_attributes}
    new_entity_attribute_dict = {single_attribute["name"]: single_attribute for single_attribute in entity_dict["entity_attributes"]}
    for key, value in entity_type_attribute_dict.items():
        if 'is_required' in value and value['is_required']:
            if key not in new_entity_attribute_dict:
                is_valid = False
                validation_msg_dict['missing_data'].append(key)
        if key in new_entity_attribute_dict:
            attribute_dict = entity_type_attribute_dict[key]
            attribute_value = new_entity_attribute_dict[key]['value']
            attribute_is_valid = validate_attribute_with_type(attribute_dict, attribute_value)
            if not attribute_is_valid:
                is_valid = False
                validation_msg_dict['data_mismatch'].append(key)
    return is_valid, validation_msg_dict


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
                "_id": str(supply_entity._id),
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
        entity_dict['created_by'] = request.user.id
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
