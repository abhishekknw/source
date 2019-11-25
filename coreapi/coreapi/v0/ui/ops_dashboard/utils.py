import logging
logger = logging.getLogger(__name__)
from v0.ui.campaign.models import CampaignComments
from v0.constants import booking_code_to_status


def getCommentsCount(campaign_id, supplier_ids):
    try:
        if len(supplier_ids) > 0:
            comments_count = CampaignComments.objects.filter(campaign_id=campaign_id,
                                                             shortlisted_spaces__object_id__in=supplier_ids).values_list(
                'shortlisted_spaces_id', flat=True).distinct().count()
            return comments_count
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None


def getEachCampaignComments(campaign_id, status_dict, supplier_dict):
    for key in status_dict.keys():
        comment_count = getCommentsCount(campaign_id, status_dict[key])
        if booking_code_to_status[key] in supplier_dict:
            supplier_dict[booking_code_to_status[key]]['comments_count'] = comment_count
            supplier_dict[booking_code_to_status[key]]['status'] = [booking_code_to_status[key]][0].lower()
            supplier_dict[booking_code_to_status[key]]['campaign_id'] = campaign_id
    return supplier_dict


def getSocietyDetails(all_supplier_dict, booking_status, supplier_detail, shortlisted_supplier):
    all_supplier_dict[booking_status]['supplier'].append({
        'name': supplier_detail['society_name'],
        'subarea': supplier_detail['society_subarea'],
        'locality': supplier_detail['society_locality'],
        'city': supplier_detail['society_city'],
        'society_quality': supplier_detail['society_type_quality'],
        'society_quantity': supplier_detail['society_type_quantity'],
        'supplier_id': shortlisted_supplier['object_id'],
        'payment_method': shortlisted_supplier['payment_method'],
        'is_completed': shortlisted_supplier['is_completed']
    })
    return all_supplier_dict
