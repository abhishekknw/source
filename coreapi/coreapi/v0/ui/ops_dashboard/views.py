import datetime
import dateutil.relativedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.proposal.models import ShortlistedSpaces, ProposalInfo, ProposalCenterMapping, HashTagImages
from v0.ui.inventory.models import *
from v0.ui.account.models import ContactDetails
from v0.ui.campaign.models import CampaignComments


class GetSocietyAnalytics(APIView):
    @staticmethod
    def get(request):
        try:
            city = request.GET.get('city', None)
            start_date = request.GET.get('start', None)
            if start_date:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            else:
                today = timezone.now()
                start_date = today + dateutil.relativedelta.relativedelta(months=-1)
            # Get all campaigns
            proposal_info = ProposalInfo.objects.filter(campaign_state='PTC', invoice_number__isnull=False, tentative_start_date__gte=start_date).values('proposal_id', 'name')
            data = {}
            proposals = []
            for p_info in proposal_info:
                if city:
                    proposal_city = ProposalCenterMapping.objects.filter(proposal_id=p_info['proposal_id'],
                                                                         city__icontains=city)
                    if proposal_city:
                        proposals.append({
                            'proposal_id': p_info['proposal_id'],
                            'city': proposal_city[0].city,
                            'name': p_info['name']
                        })
                    else:
                        continue
                else:
                    proposal_city = ProposalCenterMapping.objects.filter(proposal_id=p_info['proposal_id']).values('city')
                    proposals.append({
                        'proposal_id': p_info['proposal_id'],
                        'city': proposal_city[0]['city'],
                        'name': p_info['name']
                    })
            for proposal in proposals:
                shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=proposal['proposal_id']).values('object_id', 'id')
                number_of_society = len(shortlisted_spaces)
                data[proposal['proposal_id']] = {
                    'proposal_id': proposal['proposal_id'],
                    'name': proposal['name'],
                    'city': proposal['city'],
                    'number_of_society': number_of_society,
                    'flats': {
                        'filled': 0,
                        'not_filled': 0
                    },
                    'inventory': {
                        'banner_allowed': {
                            'yes': 0,
                            'no': 0
                        },
                        'stall_allowed': {
                            'yes': 0,
                            'no': 0
                        },
                        'standee_allowed': {
                            'yes': 0,
                            'no': 0
                        },
                        'poster_allowed': {
                            'yes': 0,
                            'no': 0
                        },
                        'flier_allowed': {
                            'yes': 0,
                            'no': 0
                        }
                    },
                    'contact_details': {
                        'name': {
                            'filled': 0,
                            'not_filled': 0
                        },
                        'number':{
                            'filled': 0,
                            'not_filled': 0
                        }
                    },
                    'hashtag_images':{
                        'receipt': {
                            'filled': 0,
                            'not_filled': 0
                        },
                        'permission_box': {
                            'filled': 0,
                            'not_filled': 0
                        }
                    },
                    'comments': {
                        'filled': 0,
                        'not_filled': 0
                    }
                }
                if not shortlisted_spaces:
                    continue

                flats_filled = 0; flats_not_filled = 0; banner_allowed_yes = 0; banner_allowed_no = 0
                stall_allowed_yes = 0; stall_allowed_no = 0; poster_allowed_yes = 0; poster_allowed_no = 0
                standee_allowed_yes = 0; standee_allowed_no = 0; flier_allowed_yes = 0; flier_allowed_no = 0
                contact_name_filled = 0; contact_name_not_filled = 0; contact_number_filled = 0; contact_number_not_filled = 0
                permission_box_filled = 0; receipt_filled = 0; comment_filled = 0

                for space in shortlisted_spaces:
                    try:
                        supplier_details = SupplierTypeSociety.objects.filter(supplier_id=space['object_id']).values()
                    except SupplierTypeSociety.DoesNotExist:
                        supplier_details = None

                    if supplier_details and len(supplier_details) > 0:
                        # Get contact details
                        try:
                            contact_details = ContactDetails.objects.filter(object_id=space['object_id']).values()
                        except ContactDetails.DoesNotExist:
                            contact_details = None

                        if contact_details:
                            contact_name_filled += 1 if contact_details[0]['name'] else 0
                            contact_name_not_filled += 1 if not contact_details[0]['name'] else 0
                            contact_number_filled += 1 if contact_details[0]['mobile'] else 0
                            contact_number_not_filled += 1 if not contact_details[0]['mobile'] else 0
                        else:
                            contact_name_not_filled += 1
                            contact_number_not_filled += 1

                        # Get hashtag images
                        hashtag_images = HashTagImages.objects.filter(object_id=space['object_id']).values('hashtag', 'image_path')
                        if hashtag_images and len(hashtag_images) > 0:
                            hashtag_image = hashtag_images[0]
                            hashtag = hashtag_image['hashtag']
                            if hashtag in ['receipt', 'Receipt', 'RECEIPT']:
                                receipt_filled += 1
                            if hashtag in ['permission_box', 'Permission Box', 'PERMISSION BOX', 'permission box']:
                                permission_box_filled += 1
                        # Get Comments
                        comments = CampaignComments.objects.filter(campaign_id=proposal['proposal_id'], shortlisted_spaces_id=space['id']).values('comment', 'related_to')
                        if comments and len(comments) > 0:
                            comment = comments[0]
                            if comment and len(comment['comment']) > 0:
                                comment_filled += 1

                        flats_filled += 1 if supplier_details[0]['flat_count'] else 0
                        flats_not_filled += 1 if not supplier_details[0]['flat_count'] else 0
                        banner_allowed_yes += 1 if supplier_details[0]['banner_allowed'] == 1 else 0
                        banner_allowed_no += 1 if supplier_details[0]['banner_allowed'] == 0 else 0
                        stall_allowed_yes += 1 if supplier_details[0]['stall_allowed'] == 1 else 0
                        stall_allowed_no += 1 if supplier_details[0]['stall_allowed'] == 0 else 0
                        poster_allowed_yes += 1 if supplier_details[0]['poster_allowed_nb'] == 1 else 0
                        poster_allowed_no += 1 if supplier_details[0]['poster_allowed_nb'] == 0 else 0
                        standee_allowed_yes += 1 if supplier_details[0]['standee_allowed'] == 1 else 0
                        standee_allowed_no += 1 if supplier_details[0]['standee_allowed'] == 0 else 0
                        flier_allowed_yes += 1 if supplier_details[0]['flier_allowed'] == 1 else 0
                        flier_allowed_no += 1 if supplier_details[0]['flier_allowed'] == 0 else 0
                        # Update data
                        data[proposal['proposal_id']]['flats']['filled'] = flats_filled
                        data[proposal['proposal_id']]['flats']['not_filled'] = flats_not_filled
                        data[proposal['proposal_id']]['inventory']['banner_allowed']['yes'] = banner_allowed_yes
                        data[proposal['proposal_id']]['inventory']['banner_allowed']['no'] = banner_allowed_no
                        data[proposal['proposal_id']]['inventory']['poster_allowed']['yes'] = poster_allowed_yes
                        data[proposal['proposal_id']]['inventory']['poster_allowed']['no'] = poster_allowed_no
                        data[proposal['proposal_id']]['inventory']['stall_allowed']['yes'] = stall_allowed_yes
                        data[proposal['proposal_id']]['inventory']['stall_allowed']['no'] = stall_allowed_no
                        data[proposal['proposal_id']]['inventory']['standee_allowed']['yes'] = standee_allowed_yes
                        data[proposal['proposal_id']]['inventory']['standee_allowed']['no'] = standee_allowed_no
                        data[proposal['proposal_id']]['inventory']['flier_allowed']['yes'] = flier_allowed_yes
                        data[proposal['proposal_id']]['inventory']['flier_allowed']['no'] = flier_allowed_no
                        data[proposal['proposal_id']]['contact_details']['name']['filled'] = contact_name_filled
                        data[proposal['proposal_id']]['contact_details']['name']['not_filled'] = contact_name_not_filled
                        data[proposal['proposal_id']]['contact_details']['number']['filled'] = contact_number_filled
                        data[proposal['proposal_id']]['contact_details']['number']['not_filled'] = contact_number_not_filled
                        data[proposal['proposal_id']]['hashtag_images']['receipt']['filled'] = receipt_filled
                        data[proposal['proposal_id']]['hashtag_images']['receipt']['not_filled'] = number_of_society - receipt_filled
                        data[proposal['proposal_id']]['hashtag_images']['permission_box']['filled'] = permission_box_filled
                        data[proposal['proposal_id']]['hashtag_images']['permission_box']['not_filled'] = number_of_society - permission_box_filled
                        data[proposal['proposal_id']]['comments']['filled'] = comment_filled
                        data[proposal['proposal_id']]['comments']['not_filled'] = number_of_society - comment_filled

            return Response(data={"status": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)