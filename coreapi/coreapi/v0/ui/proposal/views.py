from rest_framework import viewsets
from models import SupplierPhase
from serializers import SupplierPhaseSerializer
from v0.ui.utils import handle_response

class SupplierPhaseViewSet(viewsets.ViewSet):

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id')
            phases = SupplierPhase.objects.filter(campaign=campaign_id)
            serializer = SupplierPhaseSerializer(phases, many=True)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)