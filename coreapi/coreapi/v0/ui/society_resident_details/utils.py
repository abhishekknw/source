import datetime
from django.db import connection
from v0.ui.supplier.models import SupplierTypeSociety
from .models import User, ResidentDetail,ResidentCampaignDetail
from v0.ui.common.models import mongo_client
from v0.ui.proposal.models import ShortlistedSpaces, SupplierPhase
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.inventory.models import InventoryActivity, InventoryActivityAssignment


def custom_sql_query(query, data):
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        rows = cursor.fetchall()
    return rows


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


def match_resident_society_with_campaign(campaign_id, society_ids):
    spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id, object_id__in=society_ids).values('object_id')
    society_id = society_ids[0]
    if spaces and len(spaces) > 0:
        for space in spaces:
            society_id = space['object_id']
    # Add society to the campaign
    shortlisted_spaces_object = ShortlistedSpaces.objects.filter(proposal_id=campaign_id)
    shortlisted_spaces_object.object_id = society_id
    shortlisted_spaces_object.save()
    return society_id


def get_phase_id(campaign_id, lead_creation_date, society_id=None):
    supplier_phase = SupplierPhase.objects.filter(campaign_id=campaign_id).values('phase_no', 'start_date')
    sql_query = '''Select iaa.activity_date from shortlisted_spaces as ss 
    join shortlisted_inventory_pricing_details as sip 
    on ss.id=sip.shortlisted_spaces_id join inventory_activity as ia 
    on ia.shortlisted_inventory_details_id=sip.id
    join inventory_activity_assignment as iaa 
    on iaa.inventory_activity_id=ia.id
    where ia.activity_type="RELEASE" and ss.proposal_id=(%s)'''

    release_dates = custom_sql_query(sql_query, [campaign_id])
    print(release_dates)
    phase_number = 1
    for release_date in release_dates:
        for phase in supplier_phase:
            if phase['start_date'] == release_date[0]['release_date']:
                phase_number = phase['phase_no']
    return phase_number


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


def segregate_lead_data(contact_number, campaign_id, lead_creation_date, society_id=None):
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
        mongo_client.leads({'phone_number': contact_number, 'campaign_id':campaign_id, 'is_suspense': True})
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

