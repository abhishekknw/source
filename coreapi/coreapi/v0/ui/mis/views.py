from rest_framework.views import APIView
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.models import SupplierTypeSociety, SupplierTypeRetailShop
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer
from v0.ui.leads.models import (get_leads_summary)
from v0.ui.utils import handle_response

class GetMISData(APIView):
    @staticmethod
    def post(request):
        data = request.data
        supplier_ids = ShortlistedSpaces.objects.filter(proposal_id=data['campaign_id']).values('object_id')
        suppliers = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids,flat_count__gte=data['flat_count_gt'],
                                                       flat_count__lte=data['flat_count_lt'])
        serializer = SupplierTypeSocietySerializer(suppliers,many=True)

        leads_data = get_leads_summary([data['campaign_id']])
        supplier_id_with_leads_map = { supplier['supplier_id']:supplier for supplier in leads_data}
        for supplier in serializer.data:
            if supplier['supplier_id'] in supplier_id_with_leads_map:
                supplier['total_leads'] = supplier_id_with_leads_map[supplier['supplier_id']]['total_leads_count']
                supplier['hot_leads'] = supplier_id_with_leads_map[supplier['supplier_id']]['hot_leads_count']
                # supplier['lead_date'] = supplier_id_with_leads_map[supplier['supplier_id']]['created_at']
                supplier['total_leads_percentage'] = supplier_id_with_leads_map[supplier['supplier_id']][
                                                         'total_leads_count'] / supplier['flat_count'] * 100
                supplier['hot_leads_percentage'] = supplier_id_with_leads_map[supplier['supplier_id']][
                                                         'hot_leads_count'] / supplier['flat_count'] * 100


        return handle_response('', data=serializer.data, success=True)
