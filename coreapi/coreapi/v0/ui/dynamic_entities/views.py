from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from models import SupplyEntityType
from bson.objectid import ObjectId


class EntityType(APIView):
    @staticmethod
    def post(request):
        name = request.data['name']
        entity_attributes = request.data['entity_attributes']
        SupplyEntityType(**{'name': name, "entity_attributes": entity_attributes}).save()
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

class EntityTypeGetOne(APIView):
    @staticmethod
    def get(request, entity_type_id):
        supply_entity_type = SupplyEntityType.objects.raw({'_id':ObjectId(entity_type_id)})[0]
        supply_entity_type = {
            "_id": str(supply_entity_type._id),
            "name": supply_entity_type.name,
            "entity_attributes": supply_entity_type.entity_attributes
        }
        return ui_utils.handle_response('', data=supply_entity_type, success=True)
