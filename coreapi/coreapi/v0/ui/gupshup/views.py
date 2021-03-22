from __future__ import print_function
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import (Gupshup,ContactVerification, MessageTemplate)
# from .serializers import NotificationTemplateSerializer,PaymentDetailsSerializer,LicenseDetailsSerializer,RequirementSerializer, PreRequirementSerializer, RelationshipManagerSerializer
import v0.ui.utils as ui_utils
from openpyxl import load_workbook, Workbook
# from v0.ui.account.models import ContactDetails, BusinessTypes, BusinessSubTypes
# from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
# from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, ProposalCenterMapping
# from v0.ui.proposal.serializers import ProposalInfoSerializer
# from v0.ui.organisation.models import Organisation
# from v0.ui.organisation.serializers import OrganisationSerializer
from django.db.models import Q
import v0.ui.utils as ui_utils
import datetime
from v0.ui.common.models import mongo_client
import hashlib
from v0.ui.common.pagination import paginateMongo
from bson.objectid import ObjectId
# from v0.ui.common.serializers import BaseUserSerializer
# from v0.ui.supplier.serializers import SupplierMasterSerializer, SupplierTypeSocietySerializer
import v0.constants as v0_constants
from v0.constants import (campaign_status, proposal_on_hold)
from v0.ui.website.utils import manipulate_object_key_values, manipulate_master_to_rs
import v0.ui.gupshup.utils as gupshup_utils
from django.db.models import F
from v0.ui.campaign.models import CampaignComments
from datetime import timedelta
from django.utils.timezone import make_aware
from v0.constants import supplier_code_to_names
from v0.ui.supplier.views import update_contact_and_ownership_detail

from rest_framework.permissions import AllowAny
from rest_framework import permissions


class PublicEndpoint(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

class GetGupshupMsg(APIView):

    permission_classes = (PublicEndpoint,)
    def post(self, request):
        response = request.data
        template = ""
        mobile_split = None
        if response['type'] == "message-event":
            payload = request.data["payload"]
            mobile = payload.get("destination")
            mobile_split = mobile[2:12]

        if response['type'] == "message":
            payload = request.data["payload"]
            mobile = payload.get("source")
            text = response['payload']['payload']['text']

            if mobile:
                mobile_split = mobile[2:12]
                # obj = {
                # "mobile":mobile_split,
                # "message":"hello world"
                # }

                # gupshup_utils.waiting_response(obj)

                where = {"mobile":mobile_split}
                verification = mongo_client.ContactVerification.find_one(where)

                if verification:

                    if verification['verification_status'] == 2:
                        template = gupshup_utils.get_template(verification)
                        gupshup_utils.update_supplier_details(verification)
                    else:
                        context = {"_id":verification['_id'],"text":text,
                        "level":verification['level']}
                        gupshup_utils.save_response(context)

                        verify = mongo_client.ContactVerification.find_one(where)
                        if verify:
                            if verify['verification_status'] is not 2:
                                objct = {"mobile":mobile_split,"message":text}
                                message = gupshup_utils.get_response_template_without_verify(objct)
                                if message:
                                    template = message
                            else:
                                template = gupshup_utils.get_template(verify)
                                gupshup_utils.update_supplier_details(verify)
                            
                else:
                    gupshup_utils.mobile_verification(mobile_split)

                    verify = mongo_client.ContactVerification.find_one(where)
                    if verify:
                        template = gupshup_utils.get_template(verify)

                objct = {"mobile":mobile_split,"message":text}
                message = gupshup_utils.get_response_template(objct)
                if message:
                    template = message
                    res = gupshup_utils.waiting_response(objct)
                    print(res)
        if mobile_split:
            data = {"data":response,"mobile":mobile_split,"type":response['type']}
            mongo_client.gupshup.insert_one(data)
          
        return HttpResponse(template)


class SendGupshupMsg(APIView):

    permission_classes = (PublicEndpoint,)
    def post(self, request):

        msg = request.data
        URL = "https://api.gupshup.io/sm/api/v1/msg"
        params = {
                "channel" : "whatsapp",
                "source" : "917834811114",
                "destination" : "919713198098",
                "src.name":"MachadaloBot1",
                "message" : "Hi John, your order is confirmed and will be delivered to you by 15 Feb"
            }

        headers = {'Content-Type': 'application/x-www-form-urlencoded','apikey':"yvbving75adlrx2a0asejuffagte6l04"}
        r = requests.post(URL, data=params, headers=headers)
        print(r.text)
        
        return ui_utils.handle_response({}, data={"result":r.text}, success=True)
