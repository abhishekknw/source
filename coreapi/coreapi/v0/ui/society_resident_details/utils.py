import datetime
from datetime import timedelta
from v0.ui.supplier.models import SupplierTypeSociety
from .models import User, ResidentDetail,ResidentCampaignDetail
from v0.ui.common.models import mongo_client
from V0.ui.proposal.models import ShortlistedSpaces


def get_supplier(supplier_id):
    society = SupplierTypeSociety.objects.filter(supplier_id=supplier_id).values('society_name')
    if society:
        return society[0]['society_name']
    else:
        return None


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
    return int(contact_number) if contact_number else None


def check_society(campaign_id, society_ids):
    society_ids_in_campaign = ShortlistedSpaces.objects.filter(proposal_id=campaign_id, object_id__in=society_ids)

    for items in society_ids_in_campaign:
        society_id= items.object_id
        phase_number = items.phase_no
        phase = items.phase





def create_resident_and_campaign(user_id, society_id, campaign_id, timestamp):
    # Check if supplier is society
    society_name = get_supplier(society_id)
    resident_id = None
    if society_name:
        society_details = {
            'name': society_name,
            'society_id': society_id
        }
        resident_detail = {
            'user_id': user_id,
            'society_details': society_details,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        resident = ResidentDetail(**resident_detail).save()
        resident_id = str(resident._id)
    # Create resident campaign detail
    create_resident_campaign(user_id, resident_id, campaign_id, timestamp)
    return


def create_resident_campaign(user_id, resident_id, campaign_id, timestamp):
    resident_campaign_exists = mongo_client.resident_campaign_detail.find_one({
        'user_id': user_id,
        'campaign_id': campaign_id
    }, {'_id': 1})
    if not resident_campaign_exists:
        # Create resident campaign detail
        resident_campaign_detail = {
            'user_id': user_id,
            'resident_id': resident_id,
            'campaign_id': campaign_id,
            'created_at': timestamp,
            'updated_at': timestamp,
        }
        ResidentCampaignDetail(**resident_campaign_detail).save()
    return

def pull_leads():
    current_date = datetime.datetime.now().date()
    # end_date = current_date + datetime.timedelta(days=1)
    date_time = current_date - datetime.timedelta(hours=24)
    # timestamp = datetime.datetime.utcnow()

    # leads_within_twenty_four_hr = mongo_client.leads.find()
    all_leads = mongo_client.leads.find({'created_at': {"$gte": date_time}})

    all_phone_numbers = []
    all_phase_numbers = []
    all_campaign_ids = []
    all_supplier_ids = []

    for values in all_leads:
        all_supplier_ids['supplier_id'] = values.supplier_id
        all_campaign_ids['campaign_id'] = values.campaign_id
        all_phase_numbers['phase_number'] = values.phase_number
        all_phone_numbers['phone_number'] = values.phone_number
        created_at = values.created_at




    segregate_leads(contact_number, campaign_id, lead_creation_date, society_id)


def segregate_leads(contact_number, campaign_id, lead_creation_date, society_id=None):
    # Check user
    timestamp = datetime.datetime.utcnow()
    user_exists = mongo_client.user.find_one({'contact_number': contact_number}, {'_id': 1})
    if not user_exists:
        # Create user
        user_data = {
            'contact_number': contact_number,
            'created_at': timestamp,
            'updated_at': timestamp
        }
        user = User(**user_data).save()
        user_id = str(user._id)
        if society_id:
            create_resident_and_campaign(user_id, society_id, campaign_id, timestamp)

        # Create suspense lead
        mongo_client.leads.update({'phone_number': contact_number, 'campaign_id':campaign_id}, {"$set": {'is_suspense': True}})
        return
    else:
        user_id = str(user_exists._id)
        # Check resident on basis of user_id
        resident_exists = mongo_client.resident_detail.find_one({'user_id': user_id}, {'_id': 1, 'society_details': 1})
        if not resident_exists:
            if society_id:
                create_resident_and_campaign(user_id, society_id, campaign_id, timestamp)

        else:
            resident_id = str(resident_exists._id)
            # Check if given society exists in resident
            society_details = resident_exists.society_details
            society_ids = [society['society_id'] for society in society_details]

            if society_id in society_ids:
                create_resident_campaign(user_id, resident_id, campaign_id, timestamp)

