from rest_framework.response import Response
from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from v0.ui.account.models import ContactDetails

class MobileNumberVerification(APIView):

    def get(self, request):
        phone_numers = request.query_params.get("phone_number")
        contact_details = ContactDetails.objects.filter(mobile=phone_numers)
        row = {}
        if contact_details:
            row["is_exist"] = "yes"
        else:
            row["is_exist"] = "no"
        return ui_utils.handle_response({}, data=row, success=True)