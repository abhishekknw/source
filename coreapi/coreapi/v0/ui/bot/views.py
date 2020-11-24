from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from v0.ui.account.models import ContactDetails
from v0.ui.common.models import mongo_client

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

        mongo_client.bot_requirement.insert({
            "data" : data,
            "mobile" : data.get("mobile"),
            "sector" : data.get("sector"),	
            "sub_sector" : data.get("sub_sector"),
            "current_partner_feedBack" : data.get("current_partner_feedBack"),
            "preferred_partner" : data.get("preferred_partner"),
            "L1_answers" :	data.get("L1_answers"),
            "L2_answers" :	data.get("L2_answers"),
            "implementation_time"  : data.get("implementation_time"),
            "meeting_time" : data.get("meeting_time"),
            "lead_status" :	data.get("lead_status"),
            "comment" :	data.get("comment"),
            "lead_given_by" : data.get("lead_given_by"),
        })
        
        return ui_utils.handle_response({}, data=" Bot data successfully updated ", success=True)