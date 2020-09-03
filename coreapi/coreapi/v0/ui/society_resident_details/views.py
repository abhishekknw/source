import datetime
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from pymongo.errors import CursorNotFound
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from v0.ui.common.models import mongo_client
from .models import User, ResidentDetail,ResidentCampaignDetail
from .utils import get_supplier, get_last_24_hour_leads
logger = logging.getLogger(__name__)


class UpdateResident(APIView):
    @staticmethod
    def post(request):
        try:
            timestamp = datetime.datetime.utcnow()
            all_leads = mongo_client.leads.find({'created_at': {"$gte": datetime.datetime(2016, 1, 1)}})
            for lead in all_leads:
                if not lead or type(lead) != dict:
                    continue
                try:
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
                    resident_id = None
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
                        if item == 'phone_number' and lead[item] is not None:
                            resident_data['contact_number'] = lead[item]
                        if item == 'alternate_number' and lead[item] is not None:
                            resident_data['alternate_contact_number'] = lead[item]

                    contact_number = resident_data.get('contact_number', None)
                    alternate_contact_number = resident_data.get('alternate_contact_number', None)

                    if not contact_number and not alternate_contact_number:
                        continue

                    for data_item in lead['data']:
                        item_id_wise_dict[data_item['key_name']] = data_item

                    for data_item in item_id_wise_dict:
                        data_item_lower = data_item.lower()
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

                    if contact_number:
                        user_already_exists = mongo_client.user.find_one({'contact_number': contact_number}, {'_id': 1})
                        if not user_already_exists:
                            # Update user,resident, resident campaign model
                            user_data = {
                                'contact_number': contact_number,
                                'created_at': timestamp,
                                'updated_at': timestamp
                            }
                            if alternate_contact_number:
                                user_data['alternate_contact_number'] = alternate_contact_number
                            if resident_data.get('name', None):
                                user_data['name'] = resident_data['name'].title()
                            user = User(**user_data).save()
                            user_id = str(user._id)
                        else:
                            user_id = str(user_already_exists['_id'])
                        # Check resident on basis of user_id
                        resident_already_exists = mongo_client.resident_detail.find_one({'user_id': user_id}, {'_id': 1, 'society_details': 1}, no_cursor_timeout=True)
                        if not resident_already_exists:
                            if is_society:
                                resident_detail = {
                                    'user_id': user_id,
                                    'society_details': resident_data['society_details'],
                                    'created_at': timestamp,
                                    'updated_at': timestamp
                                }
                                resident = ResidentDetail(**resident_detail).save()
                                resident_id = str(resident._id)
                        else:
                            is_society_exists = False
                            resident_id = str(resident_already_exists['_id'])
                            for society in resident_already_exists['society_details']:
                                if supplier_id and isinstance(society, dict) and society['society_id'] == supplier_id:
                                    is_society_exists = True
                            if not is_society_exists:
                                # append society_details to resident
                                mongo_client.resident_detail.update_one(
                                    {'user_id': user_id},
                                    {'$push': {'society_details': society_details}}
                                )
                        # Check if user & campaign already exists
                        resident_campaign_already_exists = mongo_client.resident_campaign_detail.find_one({
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

                    # Create use for alternate contact number
                    if alternate_contact_number:
                        user_already_exists = mongo_client.user.find_one({'contact_number': alternate_contact_number},
                                                                         {'_id': 1})
                        if not user_already_exists:
                            # Update user,resident
                            user_data = {
                                'contact_number': alternate_contact_number,
                                'created_at': timestamp,
                                'updated_at': timestamp
                            }
                            User(**user_data).save()
                except CursorNotFound as e:
                    logger.exception('cursor not found 1:', e, lead)
                except Exception as e:
                    logger.exception('Error in leads :', e, lead)
        except CursorNotFound as e:
            logger.exception('cursor not found 2:', e)
        except Exception as e:
            logger.exception('Unexpected error :', e)

        return handle_response('', data='Data updated successfully', success=True)


class CreateUserResident(APIView):
    @staticmethod
    def post(request):
        try:
            get_last_24_hour_leads()
        except Exception as e:
            logger.exception('Unexpected error :', e)

        return handle_response('', data='Data updated successfully', success=True)
class GetResidentCount(APIView):
    @staticmethod
    def get(request):
        try:
            campaign_id = request.query_params.get('campaign_id')
            if not campaign_id:
                return Response(data={"status": False, "error": "Missing campaign id"},
                                status=status.HTTP_400_BAD_REQUEST)
            result = []
            spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id).values('object_id')
            resident_details = mongo_client.resident_detail.find({}, {'_id': 0, 'society_details': 1})
            resident_details_list = [detail['society_details'] for detail in resident_details]
            for space in spaces:
                society_resident_dict = {
                    'supplier_id': space['object_id'],
                    'resident_count': 0
                }
                for society_details in resident_details_list:
                    for society in society_details:
                        if society['society_id'] == space['object_id']:
                            society_resident_dict['resident_count'] += 1
                result.append(society_resident_dict)

            return Response(data={'status': True, 'data': result}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={'status': False, 'error': 'Error getting data'},
                            status=status.HTTP_400_BAD_REQUEST)
