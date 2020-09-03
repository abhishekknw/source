import datetime
from django.db import connection
from v0.ui.supplier.models import SupplierTypeSociety
from .models import User, ResidentDetail,ResidentCampaignDetail
from v0.ui.common.models import mongo_client
from v0.ui.proposal.models import ShortlistedSpaces, SupplierPhase, ProposalCenterMapping
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.inventory.models import InventoryActivity, InventoryActivityAssignment
from django.contrib.contenttypes.models import ContentType
import v0.ui.utils as ui_utils


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
    try:
        spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id).values('object_id')
        campaign_societies = [space['object_id'] for space in spaces] if spaces and len(spaces) > 0 else []
        society_id = None
        # Society in societies
        if len(campaign_societies) > 0:
            for society in campaign_societies:
                for society_id in society_ids:
                    if society == society_id:
                        society_id = society
                        break
        # Add society to the campaign
        if not society_id:
            # space = spaces[0] if len(spaces) > 0 else None
            # if space:
            #     space.object_id = society_ids[0]
            #     ShortlistedSpaces(space).save()
            # else:
            supplier_code = "RS"
            content_type = ui_utils.fetch_content_type(supplier_code)
            # Get centre
            proposal_center_mapping = ProposalCenterMapping.objects.filter(proposal_id=campaign_id).first()

            data = {
                'object_id': society_id,
                'proposal_id': campaign_id,
                'content_type': content_type,
                'supplier_code': supplier_code,
                'status': 'F',
                'user_id': 1,
                'center_id': proposal_center_mapping.id if proposal_center_mapping else None,
                # 'booking_status': 'BK'
            }
            obj, is_created = ShortlistedSpaces.objects.get_or_create(**data)
            obj.save()
        return True
    except Exception as e:
        print('Error in adding society to campaign :',e)
        return False


def get_phase_id(campaign_id, society_id):
    shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id, object_id=society_id).values('phase_no')
    lead_creation_date = datetime.datetime(2019, 12, 4, 0, 0).date()

    sql_query = '''Select iaa.activity_date, ss.phase_no_id from shortlisted_spaces as ss 
    join shortlisted_inventory_pricing_details as sip 
    on ss.id=sip.shortlisted_spaces_id join inventory_activity as ia 
    on ia.shortlisted_inventory_details_id=sip.id
    join inventory_activity_assignment as iaa 
    on iaa.inventory_activity_id=ia.id
    where ia.activity_type="RELEASE" and ss.proposal_id=(%s) and ss.object_id=(%r)'''

    release_dates = custom_sql_query(sql_query, [campaign_id, society_id])
    print('release_dates ',release_dates)
    # release_dates = [release_date[0].date() for release_date in release_dates]
    # phase_number = 1
    # min_diff = 100
    # min_diff_date = release_dates[0]
    # for release_date in release_dates:
    #     print(lead_creation_date, release_date)
    #     if lead_creation_date >= release_date:
    #         diff = (lead_creation_date - release_date).days
    #         print('diff =', diff, lead_creation_date, release_date)
    #         if min_diff > diff:
    #             min_diff = diff
    #             min_diff_date = release_date
    # find phase on basis of this date
    # for phase in supplier_phase:
    #     print(phase['start_date'].date(), min_diff_date)
    #     if phase['start_date'].date() == min_diff_date:
    #         phase_number = phase['phase_no']
    # return phase_number


def create_resident_and_campaign(user_id, society_id, campaign_id, timestamp):
    # Check if supplier is society
    society_name = get_supplier(society_id)
    resident_id = None
    if society_name:
        society_details = [{
            'name': society_name,
            'society_id': society_id
        }]
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


def get_last_24_hour_leads():
    current_date = datetime.date.today()
    last_24hour_date = current_date - datetime.timedelta(days=1)
    last_24hour_date = datetime.datetime.combine(last_24hour_date, datetime.time.min)
    leads = mongo_client.leads.find({'created_at': {"$gte": last_24hour_date}})
    for lead in leads:
        contact_number = lead['phone_number']
        campaign_id = lead['campaign_id']
        lead_creation_date = lead['lead_entry_date']
        supplier_id = lead['supplier_id']
        if contact_number and type(contact_number) == int:
            segregate_lead_data(contact_number, campaign_id, lead_creation_date, supplier_id)


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
        mongo_client.leads.update({'phone_number': contact_number, 'campaign_id': campaign_id}, {'$set': {'is_suspense': True}}, upsert=False)
        return
    else:
        user_id = str(user_exists['_id'])
        # Check resident on basis of user_id
        resident_exists = mongo_client.resident_detail.find_one({'user_id': user_id}, {'_id': 1, 'society_details': 1})
        if not resident_exists:
            if society_id:
                create_resident_and_campaign(user_id, society_id, campaign_id, timestamp)

        else:
            resident_id = str(resident_exists['_id'])
            # Check if given society exists in resident
            society_details = resident_exists['society_details']
            society_ids = [society['society_id'] for society in society_details]

            # Check if society exists in campaign
            match_resident_society_with_campaign(campaign_id, society_ids)
            create_resident_campaign(user_id, resident_id, campaign_id, timestamp)

