from __future__ import absolute_import
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from bson.objectid import ObjectId
import v0.ui.utils as ui_utils
from v0.ui.dynamic_suppliers.models import *
# from datetime import datetime, timedelta
import datetime

import dateutil.parser


class tappingView(APIView):

    def get(self, request, organisation_id):

        try:
            user = request.user
            from_date = request.query_params.get('from', None)
            to_date = request.query_params.get('to', None)
            query_parameter = []
            for_all_queries = {}

            if from_date and to_date: 
                start_date = dateutil.parser.parse(from_date)
                end_date = dateutil.parser.parse(to_date)
                # end_date = datetime.datetime.fromtimestamp(int(to_date)).isoformat()

                
                if start_date and end_date:
                    for_all_queries["$and"] =  query_parameter
                    query_parameter  += [
                        {'created_at':{"$gte": start_date}},
                        {'created_at':{"$lte": end_date}}
                        ]

            if not user.is_superuser:
                query_parameter.append({'organisation_id':organisation_id})

            all_supply_supplier_dict = {}
            total_found = 0
            total = 1
            contact_details_count_matched = 0
            contact_details_count_unmatched = 0
            location_details_count_matched = 0
            location_details_count_unmatched = 0

            supplier_query = SupplySupplier.objects.raw(for_all_queries)
            supplier_type_query = SupplySupplierType.objects.raw(for_all_queries)


            for supply_supplier in supplier_query:

                for supply_supplier_type in supplier_type_query:
                    supply_supplier_type_name = supply_supplier_type.name
                type_id = supply_supplier.supplier_type_id
                for key, value in supply_supplier.additional_attributes.items(): 
                    if type_id in all_supply_supplier_dict:
                        total_found += 1
                        total += 1
                        
                        if key == 'contact_details':
                            contact_details_count_matched += 1
                        if key == 'location_details':
                            location_details_count_matched += 1

                        all_supply_supplier_dict[str(supply_supplier.supplier_type_id)] = {
                            "name": supply_supplier_type_name,
                            "contact_details_count_matched": {
                                "done": contact_details_count_matched,
                                "total": total
                            },
                            "location_details_count_matched": {
                                "done": location_details_count_matched ,
                                "total": total
                            }
                        }        
                    else:

                        if key == 'contact_details':
                            contact_details_count_unmatched += 1
                        if key == 'location_details':
                            location_details_count_unmatched += 1

                        all_supply_supplier_dict[str(supply_supplier.supplier_type_id)] = {
                            "name": supply_supplier_type_name,
                            "contact_details_count_unmatched": {
                                "done": contact_details_count_unmatched,
                                "total": contact_details_count_unmatched
                            },
                            "location_details_count_unmatched": {
                                "done": location_details_count_unmatched ,
                                "total": location_details_count_unmatched
                            }
                        }
                    
            return handle_response('', data=all_supply_supplier_dict, success=True)
        except Exception as e:
            return ui_utils.handle_response('', exception_object=e, request=request)
