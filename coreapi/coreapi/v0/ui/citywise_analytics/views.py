import logging

logger = logging.getLogger(__name__)
import datetime
import dateutil.relativedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.proposal.models import ShortlistedSpaces, ProposalInfo, ProposalCenterMapping, HashTagImages, SupplierAssignment
from v0.ui.account.models import ContactDetails
from v0.ui.common.models import BaseUser
from v0.ui.campaign.models import CampaignAssignment, CampaignComments
from v0.constants import (campaign_status, proposal_on_hold, booking_code_to_status,
                          proposal_not_converted_to_campaign, booking_substatus_code_to_status,
                          proposal_finalized)


class GetCityWiseAnalytics(APIView):
    @staticmethod
    def get(self):
        try:
            return Response(data={"status": True, "data": {}}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)