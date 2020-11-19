import datetime
import logging
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from v0.ui.common.models import mongo_client
from bson.objectid import ObjectId
logger = logging.getLogger(__name__)


class updateLeadsItems(APIView):
    @staticmethod
    def patch(request):
        all_leads = mongo_client.leads.find()
        for lead in all_leads:
            item_id_wise_dict = {}
            society_details = {}
            phone_number = None
            alternate_number = None
            lead_entry_date = None
            phase_number = 1
            _id = None
            for item in lead:
                if item == 'created_at':
                    lead_entry_date = lead[item]
                if item == '_id':
               	    _id = lead[item]

            for data_item in lead['data']:
                item_id_wise_dict[data_item['key_name']] = data_item

            for data_item in item_id_wise_dict:
                data_item_lower = data_item.lower()
                if data_item_lower in ['primary number', 'contact number']:
                    if item_id_wise_dict[data_item]['value'] and item_id_wise_dict[data_item]['value'] != 'NA':
                        phone_number = format_contact_number(item_id_wise_dict[data_item]['value'])

                if data_item_lower == 'alternate number' and item_id_wise_dict[data_item]['value'] and item_id_wise_dict[data_item]['value'] != 'NA':
                    alternate_number = format_contact_number(item_id_wise_dict[data_item]['value'])
            # print(phone_number, alternate_number)
            lead_dict = {"phone_number": phone_number, "phase_number": int(phase_number), "alternate_number": alternate_number, "lead_entry_date":lead_entry_date}
            mongo_client.leads.update({"_id": _id}, {"$set": lead_dict})

        return handle_response('', data='Data updated successfully', success=True)


import math
def format_contact_number(contact_number):
    if type(contact_number) == str:
        contact_number = contact_number.replace('-', '')
        contact_number = contact_number.replace(' ', '')
        contact_number = contact_number.split('\n')[0]
        contact_number = contact_number.split('&')[0]
        contact_number = contact_number.split(',')[0]
        contact_number = contact_number.split('/')[0]
        contact_number = contact_number.split('.')[0]
        contact_number = contact_number.split('*')[0]
        if not contact_number.isdigit():
            return None
    contact_number = int(contact_number)
    if int(math.log10(contact_number)) + 1 == 10:
    	return contact_number if contact_number else None
