import datetime
import v0.ui.utils as ui_utils
from v0.ui.proposal.models import ShortlistedSpaces


def convert_xldate_as_datetime(xldate):
    return (
        datetime.datetime(1899, 12, 30) + datetime.timedelta(days=xldate + 1462 * 0)
        )


def add_society_to_campaign(campaign_id, society_id):
    try:
        supplier_code = "RS"
        content_type = ui_utils.fetch_content_type(supplier_code)
        data = {
            'object_id': society_id,
            'proposal_id': campaign_id,
            'content_type': content_type,
            # 'created_at': datetime.datetime.utcnow(),
            # 'updated_at': datetime.datetime.utcnow(),
            # 'assigned_date': datetime.datetime.utcnow()
        }
        print(data)
        obj, is_created = ShortlistedSpaces.objects.get_or_create(**data)
        obj.save()
        return True
    except Exception as e:
        print('Error in adding society to campaign :',e)
        return False