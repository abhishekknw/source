from rest_framework.views import APIView
from models import (LeadsForm, LeadsFormItems, LeadsFormData)
import v0.ui.utils as ui_utils
from celery import shared_task
from v0.ui.common.models import mongo_client


@shared_task()
def migrate_to_mongo():
    campaign_list = list(set(LeadsFormData.objects.values_list('campaign_id', flat=True)))
    for campaign_id in campaign_list:
        all_leads_data_object = LeadsFormData.objects.filter(campaign_id=campaign_id).all()
        all_leads_data = []
        for data in all_leads_data_object:
            all_leads_data.append(data.__dict__)
        all_leads_forms = LeadsForm.objects.all().values('id', 'campaign_id', 'leads_form_name', 'last_entry_id',
                                                         'status', "fields_count", "last_contact_id", "created_at")
        all_leads_items = LeadsFormItems.objects.all().values('leads_form_id', 'item_id', 'key_name', 'hot_lead_criteria',
                                                              'key_options', 'order_id', 'status', 'is_required',
                                                              'key_type',
                                                              'campaign_id', 'supplier_id')
        all_leads_items_dict = {}
        for lead_item in all_leads_items:
            if lead_item['leads_form_id'] not in all_leads_items_dict:
                all_leads_items_dict[lead_item['leads_form_id']] = []
            all_leads_items_dict[lead_item['leads_form_id']].append(lead_item)
        for leads_form in all_leads_forms:
            mongo_dict = {
                'leads_form_id': leads_form['id'],
                'campaign_id': leads_form['campaign_id'],
                'leads_form_name': leads_form['leads_form_name'],
                'last_entry_id': leads_form['last_entry_id'],
                'status': leads_form['status'],
                'last_contact_id': leads_form['last_contact_id'],
                'created_at': leads_form['created_at'],
                'data': {}
            }
            if leads_form['id'] in all_leads_items_dict:
                for item in all_leads_items_dict[leads_form['id']]:
                    key_options = item["key_options"] if 'key_options' in item else None
                    mongo_dict['data'][str(item['item_id'])] = {
                        'item_id': item['item_id'],
                        'key_type': item['key_type'],
                        'key_name': item['key_name'],
                        'key_options': key_options,
                        'order_id': item['order_id'],
                        'status': item['status'],
                        'leads_form_id': item['leads_form_id'],
                        'is_required': item['is_required'],
                        'hot_lead_criteria': item['hot_lead_criteria'],
                        'campaign_id': item['campaign_id'],
                        'supplier_id': item['supplier_id'],

                    }
            mongo_client.leads_forms.insert_one(mongo_dict)
        leads_form_ids = all_leads_data_object.values_list('leads_form_id', flat=True).distinct()
        for curr_form_id in leads_form_ids:
            curr_form_id = curr_form_id
            curr_form_data = [x for x in all_leads_data if x['leads_form_id'] == curr_form_id]
            curr_form_items = [x for x in all_leads_items if x['leads_form_id'] == curr_form_id]
            first_data_element = curr_form_data[0]
            campaign_id = first_data_element['campaign_id']
            entry_ids = list(set([x['entry_id'] for x in curr_form_data]))
            entry_count = 0
            for curr_entry_id in entry_ids:
                entry_count = entry_count + 1
                curr_entry_data = [x for x in curr_form_data if x['entry_id'] == curr_entry_id]
                supplier_id = curr_entry_data[0]['supplier_id']
                created_at = curr_entry_data[0]['created_at']
                lead_dict = {"data": [], "is_hot": False, "created_at": created_at, "supplier_id": supplier_id,
                             "campaign_id": campaign_id, "leads_form_id": curr_form_id, "entry_id": curr_entry_id,
                             "status": "active"}
                for curr_data in curr_entry_data:
                    item_id = curr_data['item_id']
                    value = curr_data['item_value']
                    curr_item = [x for x in curr_form_items if x['item_id'] == item_id][0]
                    key_name = curr_item['key_name']
                    key_type = curr_item['key_type']
                    item_dict = {
                        'item_id': item_id,
                        'key_name': key_name,
                        'value': value,
                        'key_type': key_type
                    }
                    lead_dict['data'].append(item_dict)
                    if value:
                        if curr_item['hot_lead_criteria'] and value == curr_item['hot_lead_criteria']:
                            lead_dict["is_hot"] = True
                        elif 'counseling' in key_name.lower():
                            lead_dict["is_hot"] = True
                mongo_client.leads.insert_one(lead_dict)
    return


class MigrateLeadsToMongo(APIView):
    def put(self, request):
        class_name = self.__class__.__name__
        migrate_to_mongo.delay()
        return ui_utils.handle_response(class_name, data='success', success=True)