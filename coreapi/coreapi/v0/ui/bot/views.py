from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from v0.ui.account.models import ContactDetails
from v0.ui.common.models import mongo_client
from django.db.models import Q
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
        if data['phone']:
            response = bot_utils.bot_to_requirement(request, data)        
            return ui_utils.handle_response({}, data="Bot data successfully Added", success=True)
        else:
            return ui_utils.handle_response({}, data={"errors":"Phone Number should not be null"}, success=False)
        
