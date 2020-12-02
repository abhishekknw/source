from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from v0.ui.account.models import ContactDetails
from v0.ui.common.models import mongo_client

import v0.ui.bot.utils as bot_utils

class MobileNumberVerification(APIView):
    permission_classes = ()

    def get(self, request):
        mobile = request.query_params.get("mobile")
        row = {"is_exist":"no"}
        
        if mobile.isnumeric():
            contact_details = ContactDetails.objects.filter(mobile=mobile)
            if contact_details:
                row["is_exist"] = "yes"
        return ui_utils.handle_response({}, data=row, success=True)

class GetDataFromBot(APIView):

    def post(self, request):
        data = request.data

        mobile = data.get("phone")
        sessionIds = data.get("sessionIds")
        requestId = data.get("requestId")
        datetime = data.get("datetime")

        if mobile is None:
            return ui_utils.handle_response({}, data="Phone number is Mandatory", success=False)

        phone_number = ContactDetails.objects.filter(mobile=mobile)

        if phone_number:
            for row in data["data"]:
                bot_data = list(mongo_client.bot_requirement.find({"$and":[{"mobile": mobile}, {"sector": row.get("service")}, {"subsector":row.get("subService")}]}))
                if bot_data:
                    mongo_client.bot_requirement.update({
                        "bot_data" : data,
                        "mobile" : mobile,
                        "sessionIds" : sessionIds,
                        "requestId" : requestId,
                        "datetime" : datetime,
                        "sector" : row.get("service"),	
                        "sub_sector" : row.get("subService"),
                        "L1Response_1": row.get("L1Response_1"),
                        "L1Response_2": row.get("L1Response_2"),
                        "L2Response_1": row.get("L2Response_1"),
                        "L2Response_2": row.get("L2Response_2"),
                        "current_partner" : row.get("existingPartner"),
                        "current_partner_feedBack" : row.get("partnerFeedback"),
                        "feedback_reason" : row.get("feedbackReason"),
                        "preferred_partner" : row.get("preferredPartner"),
                        "implementation_time"  : row.get("implementationTime"),
                        "meeting_time" : row.get("meetingTime"),
                        "call_back_time" : row.get("contactBackTime")
                    })
        else:
            for row in data["data"]:
                mongo_client.bot_requirement.insert({
                    "bot_data" : data,
                    "mobile" : mobile,
                    "sessionIds" : sessionIds,
                    "requestId" : requestId,
                    "datetime" : datetime,
                    "sector" : row.get("service"),	
                    "sub_sector" : row.get("subService"),
                    "L1Response_1": row.get("L1Response_1"),
                    "L1Response_2": row.get("L1Response_2"),
                    "L2Response_1": row.get("L2Response_1"),
                    "L2Response_2": row.get("L2Response_2"),
                    "current_partner" : row.get("existingPartner"),
                    "current_partner_feedBack" : row.get("partnerFeedback"),
                    "feedback_reason" : row.get("feedbackReason"),
                    "preferred_partner" : row.get("preferredPartner"),
                    "implementation_time"  : row.get("implementationTime"),
                    "meeting_time" : row.get("meetingTime"),
                    "call_back_time" : row.get("contactBackTime")
                })
        response = bot_utils.bot_to_requirement(request, data)        
        return ui_utils.handle_response({}, data="Bot data successfully Added", success=True)
