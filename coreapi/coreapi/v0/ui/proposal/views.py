from rest_framework import viewsets
from models import SupplierPhase, ProposalInfo
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

    def create(self, request):
        class_name = self.__class__.__name__
        try:
            phases = request.data
            campaign_id = request.query_params.get('campaign_id')
            for phase in phases:
                if 'id' in phase:
                    item = SupplierPhase.objects.get(pk=phase['id'],campaign=campaign_id)
                    phase_serializer = SupplierPhaseSerializer(item, data=phase)
                else:
                    phase['campaign'] = campaign_id
                    phase_serializer = SupplierPhaseSerializer(data=phase)
                if phase_serializer.is_valid():
                    phase_serializer.save()
            data = SupplierPhase.objects.filter(campaign=campaign_id)
            serializer = SupplierPhaseSerializer(data,many=True)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)
