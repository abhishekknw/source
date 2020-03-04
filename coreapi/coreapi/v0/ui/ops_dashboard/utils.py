import logging
logger = logging.getLogger(__name__)
from v0.ui.campaign.models import CampaignComments


def getCommentsCount(campaign_id, supplier_ids):
    try:
        if len(supplier_ids) > 0:
            external_comments_count = CampaignComments.objects.filter(campaign_id=campaign_id,
                                                             shortlisted_spaces__object_id__in=supplier_ids, related_to='EXTERNAL').values_list(
                'shortlisted_spaces_id', flat=True).distinct().count()
            internal_comments_count = CampaignComments.objects.filter(campaign_id=campaign_id,
                                                             shortlisted_spaces__object_id__in=supplier_ids, related_to='INTERNAL').values_list(
                'shortlisted_spaces_id', flat=True).distinct().count()
            return {
                'internal_comments_filled_count': internal_comments_count,
                'external_comments_filled_count': external_comments_count
            }
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None


def getEachCampaignComments(campaign_id, campaign_name, supplier_dict):
    for key in supplier_dict.keys():
        comments = getCommentsCount(campaign_id, supplier_dict[key]['supplier_ids'])
        internal_comments_filled_count = external_comments_filled_count = 0
        if comments is not None:
            internal_comments_filled_count = comments['internal_comments_filled_count']
            external_comments_filled_count = comments['external_comments_filled_count']
        total_suppliers = len(supplier_dict[key]['supplier_ids'])
        if key in supplier_dict:
            supplier_dict[key]['internal_comments_filled_count'] = internal_comments_filled_count
            supplier_dict[key]['external_comments_filled_count'] = external_comments_filled_count
            supplier_dict[key]['internal_comments_not_filled_count'] = total_suppliers - internal_comments_filled_count
            supplier_dict[key]['external_comments_not_filled_count'] = total_suppliers - external_comments_filled_count
            supplier_dict[key]['total_suppliers'] = total_suppliers
            supplier_dict[key]['status'] = key
            supplier_dict[key]['campaign_id'] = campaign_id
            supplier_dict[key]['campaign_name'] = campaign_name
            if total_suppliers > 0:
                supplier_dict[key]['internal_comments_filled_percentage'] = round(
                    (internal_comments_filled_count / total_suppliers) * 100, 2)
                supplier_dict[key]['internal_comments_not_filled_percentage'] = round(
                    ((total_suppliers - internal_comments_filled_count) / total_suppliers) * 100, 2)
                supplier_dict[key]['external_comments_filled_percentage'] = round(
                    (external_comments_filled_count / total_suppliers) * 100, 2)
                supplier_dict[key]['external_comments_not_filled_percentage'] = round(
                    ((total_suppliers - external_comments_filled_count) / total_suppliers) * 100, 2)
    return supplier_dict


def getSocietyDetails(all_supplier_dict, booking_status, supplier_detail, shortlisted_supplier):
    all_supplier_dict[booking_status]['supplier'].append({
        'name': supplier_detail['society_name'] if supplier_detail else '',
        'area': supplier_detail['society_locality'] if supplier_detail else '',
        'subarea': supplier_detail['society_subarea'] if supplier_detail else '',
        'city': supplier_detail['society_city'] if supplier_detail else '',
        'society_quality': supplier_detail['society_type_quality'] if supplier_detail else '',
        'supplier_id': shortlisted_supplier['object_id'] if shortlisted_supplier else '',
        'payment_method': shortlisted_supplier['payment_method'] if shortlisted_supplier else '',
        'is_completed': shortlisted_supplier['is_completed'] if shortlisted_supplier else '',
        'society_latitude': supplier_detail['society_latitude'] if supplier_detail else '',
        'society_longitude': supplier_detail['society_longitude'] if supplier_detail else '',
        'contact_number': supplier_detail['contact_number'] if supplier_detail else '',
        'contact_name': supplier_detail['contact_name'] if supplier_detail else  ''
    })
    return all_supplier_dict
