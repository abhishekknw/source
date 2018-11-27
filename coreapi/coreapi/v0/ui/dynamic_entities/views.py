from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from models import SupplyEntityType, SupplyEntity
from bson.objectid import ObjectId
from datetime import datetime
from v0.ui.account.models import Profile


class EntityType(APIView):
    @staticmethod
    def post(request):
        name = request.data['name']
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        entity_attributes = request.data['entity_attributes']
        profile_id = request.user.profile_id
        profile = Profile.objects.filter(id=profile_id).all()
        if len(profile) == 0:
            return
        organisation_id = profile[0].organisation_id
        dict_of_req_attributes = {"name": name, "entity_attributes": entity_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return ui_utils.handle_response('', data=validation_msg_dict, success=False)
        SupplyEntityType(**{'name': name, "entity_attributes": entity_attributes, "organisation_id": organisation_id,
                            "is_global": is_global, "created_at": datetime.now()}).save()
        return ui_utils.handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_supply_entity_type = SupplyEntityType.objects.all()
        all_supply_entity_type_dict = {}
        for supply_entity_type in all_supply_entity_type:
            print supply_entity_type._id, type(supply_entity_type._id)
            all_supply_entity_type_dict[str(supply_entity_type._id)] = {
                "_id": str(supply_entity_type._id),
                "name": supply_entity_type.name,
                "entity_attributes": supply_entity_type.entity_attributes
            }
        return ui_utils.handle_response('', data=all_supply_entity_type_dict, success=True)


class EntityTypeById(APIView):
    @staticmethod
    def get(request, entity_type_id):
        supply_entity_type = SupplyEntityType.objects.raw({'_id':ObjectId(entity_type_id)})[0]
        supply_entity_type = {
            "_id": str(supply_entity_type._id),
            "name": supply_entity_type.name,
            "entity_attributes": supply_entity_type.entity_attributes
        }
        return ui_utils.handle_response('', data=supply_entity_type, success=True)


    @staticmethod
    def put(request, entity_type_id):
        new_name = request.data['name'] if 'name' in request.data else None
        new_attributes = request.data['entity_attributes'] if 'entity_attributes' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        exist_entity_query = SupplyEntityType.objects.raw({'_id': ObjectId(entity_type_id)})[0]
        dict_of_req_attributes = {"name": new_name, "entity_attributes": new_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return ui_utils.handle_response('', data=validation_msg_dict, success=False)
        exist_entity_query.name = new_name
        exist_entity_query.entity_attributes = new_attributes
        exist_entity_query.is_global = is_global
        exist_entity_query.updated_at = datetime.now()
        exist_entity_query.save()
        return ui_utils.handle_response('', data="success", success=True)


    @staticmethod
    def delete(request, entity_type_id):
        exist_entity_query = SupplyEntityType.objects.raw({'_id': ObjectId(entity_type_id)})[0]
        exist_entity_query.delete()
        return ui_utils.handle_response('', data="success", success=True)


def create_validation_msg(dict_of_required_attributes):
    is_valid = True
    validation_msg_dict = {'missing_data':[]}
    for key, value in dict_of_required_attributes.items():
        if not value:
            is_valid = False
            validation_msg_dict['missing_data'].append(key)
    return (is_valid, validation_msg_dict)


class Entity(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        entity_type_id = request.data['entity_type_id'] if 'entity_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        entity_attributes = request.data['entity_attributes']
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None
        dict_of_req_attributes = {"name": name, "entity_type_id": entity_type_id, "is_custom": is_custom,
             "entity_attributes": entity_attributes, "supplier_id": supplier_id, "campaign_id": campaign_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        entity_dict = dict_of_req_attributes
        entity_dict['created_by'] = request.user.id
        profile_id = request.user.profile_id
        profile = Profile.objects.filter(id=profile_id).all()
        if len(profile) == 0:
            return
        entity_dict['organisation_id'] = profile[0].organisation_id
        entity_dict['created_at'] = datetime.now()
        if not is_valid:
            return ui_utils.handle_response('', data=validation_msg_dict, success=False)
        SupplyEntity(**entity_dict).save()
        return ui_utils.handle_response('', data={"success": True}, success=True)


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
                "supplier_id": supply_entity.supplier_id,
                "campaign_id": supply_entity.campaign_id,
                "created_at": supply_entity.created_at,
            }
        return ui_utils.handle_response('', data=all_supply_entity_dict, success=True)


class EntityById(APIView):
    @staticmethod
    def put(request, entity_id):
        name = request.data['name'] if 'name' in request.data else None
        entity_type_id = request.data['entity_type_id'] if 'entity_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        entity_attributes = request.data['entity_attributes']
        supplier_id = request.data['supplier_id'] if 'supplier_id' in request.data else None
        campaign_id = request.data['campaign_id'] if 'campaign_id' in request.data else None
        dict_of_req_attributes = {"name": name, "entity_type_id": entity_type_id, "is_custom": is_custom,
             "entity_attributes": entity_attributes, "supplier_id": supplier_id, "campaign_id": campaign_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        entity_dict = dict_of_req_attributes
        entity_dict['created_by'] = request.user.id
        profile_id = request.user.profile_id
        profile = Profile.objects.filter(id=profile_id).all()
        if len(profile) == 0:
            return
        entity_dict['organisation_id'] = profile[0].organisation_id
        entity_dict['updated_at'] = datetime.now()
        if not is_valid:
            return ui_utils.handle_response('', data=validation_msg_dict, success=False)
        SupplyEntity.objects.raw({'_id': ObjectId(entity_id)}).update({"$set": entity_dict})
        return ui_utils.handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, entity_id):
        exist_entity_query = SupplyEntity.objects.raw({'_id': ObjectId(entity_id)})[0]
        exist_entity_query.delete()
        return ui_utils.handle_response('', data="success", success=True)
