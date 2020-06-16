import datetime
import logging
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from v0.ui.common.models import mongo_client
from bson.objectid import ObjectId
from .models import User, ResidentDetail,ResidentCampaignDetail
from .utils import get_supplier, format_contact_number
logger = logging.getLogger(__name__)


class UpdateResident(APIView):
    @staticmethod
    def post(request):
        timestamp = datetime.datetime.utcnow()
        all_leads = mongo_client.leads.find()
        for lead in all_leads:
            resident_data = {
                'society_details': [],
                'lead_phases': {
                    'impression': False,
                    'click': False,
                    'lead': True,
                    'hot_lead': False,
                    'in_between': False,
                    'converted': False
                }
            }
            item_id_wise_dict = {}
            society_details = {}
            is_society = False
            supplier_id = None
            for item in lead:
                if item == 'supplier_id':
                    supplier_id = lead[item]
                    resident_data['supplier_id'] = supplier_id
                    # Check if supplier is society
                    society_name = get_supplier(supplier_id)
                    if society_name:
                        society_details['name'] = society_name
                        society_details['society_id'] = supplier_id
                        is_society = True
                if item == 'campaign_id':
                    resident_data['campaign_id'] = lead[item]
                if item == 'is_hot':
                    resident_data['lead_phases']['hot_lead'] = True if lead[item] else False
                if item == 'hotness_level':
                    resident_data['hotness_level'] = lead[item]

            for data_item in lead['data']:
                item_id_wise_dict[data_item['key_name']] = data_item

            for data_item in item_id_wise_dict:
                data_item_lower = data_item.lower()
                if data_item_lower in ['primary number', 'contact number']:
                    if item_id_wise_dict[data_item]['value'] and item_id_wise_dict[data_item]['value'] != 'NA':
                        contact_number = format_contact_number(item_id_wise_dict[data_item]['value'])
                        print('contact_number', contact_number)
                        if contact_number:
                            resident_data['contact_number'] = contact_number
                if data_item_lower == 'alternate number' and item_id_wise_dict[data_item]['value'] and item_id_wise_dict[data_item]['value'] != 'NA':
                    alternate_contact_number = format_contact_number(item_id_wise_dict[data_item]['value'])
                    print('alternate_contact_number', alternate_contact_number)
                    if alternate_contact_number:
                        resident_data['alternate_contact_number'] = alternate_contact_number
                if data_item_lower in ['parent name', 'name']:
                    resident_data['name'] = item_id_wise_dict[data_item]['value']
                if data_item_lower == 'apartment_name':
                    society_details['apartment_name'] = item_id_wise_dict[data_item]['value']
                if data_item_lower == 'area':
                    society_details['area'] = item_id_wise_dict[data_item]['value']
                if data_item_lower in ['tower / wing', 'tower', 'tower/wing']:
                    society_details['tower'] = item_id_wise_dict[data_item]['value']
                if data_item_lower in ['flat no', 'flat number', 'flat no.']:
                    society_details['flat_number'] = item_id_wise_dict[data_item]['value']
            resident_data['society_details'].append(society_details)
            # Check if user, resident exists
            if 'contact_number' in resident_data:
                user_already_exists = mongo_client.user.find_one({'contact_number': resident_data['contact_number']}, {'_id': 1})
                if not user_already_exists:
                    # Update user,resident, resident campaign model
                    user_data = {
                        'contact_number': resident_data['contact_number'],
                        'created_at': timestamp,
                        'updated_at': timestamp
                    }
                    if 'alternate_contact_number' in resident_data:
                        user_data['alternate_contact_number'] = resident_data['alternate_contact_number']
                    user = User(**user_data).save()
                    user_id = user._id
                else:
                    user_id = user_already_exists['_id']
                # Check resident on basis of user_id
                resident_already_exists = mongo_client.resident_details.find_one({'user_id': user_id}, {'_id': 1, 'society_details': 1})
                if not resident_already_exists:
                    if is_society:
                        resident_detail = {
                            'user_id': user_id,
                            'society_details': resident_data['society_details'],
                            'created_at': timestamp,
                            'updated_at': timestamp
                        }
                        resident = ResidentDetail(**resident_detail).save()
                        resident_id = resident._id
                else:
                    resident_id = resident_already_exists['_id']

                    for society_details in resident_already_exists['society_details']:
                        if supplier_id and society_details.get('society_id') != supplier_id:
                            # append society_details to resident
                            resident_already_exists.update_one(
                                {"user_id": user_id},
                                {"$push": {society_details: society_details}}
                            )
                # Check if user & campaign already exists
                resident_campaign_already_exists = mongo_client.resident_campaign_details.find_one({
                    'user_id': user_id,
                    'campaign_id': resident_data['campaign_id']
                }, {'_id': 1})
                if not resident_campaign_already_exists:
                    resident_campaign_detail = {
                        'user_id': user_id,
                        'campaign_id': resident_data['campaign_id'],
                        'lead_phases': resident_data['lead_phases'],
                        'created_at': timestamp,
                        'updated_at': timestamp,
                    }
                    if resident_id:
                        resident_campaign_detail['resident_id'] = resident_id
                    ResidentCampaignDetail(**resident_campaign_detail).save()
            else:
                logger.exception('No contact number present in lead')
        return handle_response('', data='Data updated successfully', success=True)

