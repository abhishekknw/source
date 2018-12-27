from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from v0.ui.common.models import mongo_client, mongo_test
from bson.objectid import ObjectId


class UpdateLeadsMissingItems(APIView):
    @staticmethod
    def put(request):
        all_leads_forms = list(mongo_client.leads_forms.find())
        all_leads_forms_dict = {leads_form["leads_form_id"]:leads_form for leads_form in all_leads_forms}
        all_leads = mongo_client.leads.find()
        for lead in all_leads:
            item_id_wise_dict = {}
            item_id_wise_final_dict = {}
            max_item_id = 0
            for data_item in lead["data"]:
                item_id_wise_dict[data_item["item_id"]] = data_item
            for data_item_idx in all_leads_forms_dict[lead["leads_form_id"]]["data"]:
                data_item = all_leads_forms_dict[lead["leads_form_id"]]["data"][data_item_idx]
                if data_item["item_id"] in item_id_wise_dict:
                    item_id_wise_final_dict[data_item["item_id"]] = item_id_wise_dict[data_item["item_id"]]
                    if "value" not in item_id_wise_final_dict[data_item["item_id"]]:
                        item_id_wise_final_dict[data_item["item_id"]]["value"] = None
                else:
                    item_id_wise_final_dict[data_item["item_id"]] = {
                        "item_id": data_item["item_id"],
                        "key_name": data_item["key_name"],
                        "key_options": data_item["key_options"] if "key_options" in data_item else None,
                        "key_type": data_item["key_type"] if "key_type" in data_item else None,
                        "is_required": data_item["is_required"] if "is_required" in data_item else None,
                        "order_id": data_item["order_id"] if "order_id" in data_item else None,
                        "value": None
                    }
                if data_item["item_id"] > max_item_id:
                    max_item_id = data_item["item_id"]
            final_data_list = []
            for item_id in range(1,max_item_id+1):
                final_data_list.append(item_id_wise_final_dict[item_id])
            mongo_client.leads.update_one({"_id": ObjectId(str(lead["_id"]))},
                                          {"$set": {"data": final_data_list}})
        return handle_response('', data={"success": True}, success=True)


class UpdateLeadsEntryIds(APIView):
    @staticmethod
    def put(request):
        all_leads_forms = list(mongo_client.leads_forms.find())
        for leads_form in all_leads_forms:
            leads_form_id = leads_form["leads_form_id"]
            entry_id = 0
            all_leads_form_leads = mongo_client.leads.find({"leads_form_id": int(leads_form_id)}).sort("created_at", 1)
            for lead in all_leads_form_leads:
                entry_id = entry_id + 1
                _id = ObjectId(str(lead["_id"]))
                mongo_client.leads.update_one({"_id":_id}, {"$set": {"entry_id": entry_id}})
            mongo_client.leads_forms.update_one({"leads_form_id": leads_form_id},
                                                {"$set": {"last_entry_id": entry_id}})
        return handle_response('', data={"success": True}, success=True)
