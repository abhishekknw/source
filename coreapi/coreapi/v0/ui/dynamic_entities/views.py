from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from models import SupplyEntityType


class CreateEntityType(APIView):
    @staticmethod
    def post(request):
        name = request.data['name']
        entity_attributes = request.data['entity_attributes']
        SupplyEntityType(**{'name': name, "entity_attributes": entity_attributes}).save()
        return ui_utils.handle_response('', data={"success": True}, success=True)
