from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from v0.ui.account.models import ContactDetails, BusinessTypes, BusinessSubTypes
from v0.ui.common.models import mongo_client
from django.db.models import Q
import v0.ui.bot.utils as bot_utils
import requests
import json
from openpyxl import load_workbook, Workbook
from django.http import HttpResponse
import v0.ui.b2b.utils as b2b_utils
from v0.ui.organisation.models import Organisation

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
        mongo_client.bot_log.insert_one(data)
        if data['phone']:
            response = bot_utils.bot_to_requirement(request, data)        
            return ui_utils.handle_response({}, data="Bot data successfully Added", success=True)
        else:
            return ui_utils.handle_response({}, data={"errors":"Phone Number should not be null"}, success=False)
        
class AlternateApiGetDataFromBot(APIView):

    def post(self, request):
        data = request.data
        if data['phone']:
            response = bot_utils.bot_to_requirement(request, data)        
            return ui_utils.handle_response({}, data="Bot data successfully Added", success=True)
        else:
            return ui_utils.handle_response({}, data={"errors":"Phone Number should not be null"}, success=False)


class GetDataFromBotToSheet(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):

        mobile = request.query_params.get("mobile")
        end_date = request.query_params.get("end_date")
        start_date = request.query_params.get("start_date")

        API_ENDPOINT = "http://35.226.184.99:5002/v1/bot_data/getLeads"

        data = {
            "mobile" : mobile,
            "fromDate" : start_date,
            "toDate" : end_date}
        r = requests.post(url = API_ENDPOINT, data = data)

        pastebin_url = r.text
        
        y = json.loads(pastebin_url)

        if pastebin_url:

            header_list = ['Phone Number', 'Supplier Name', 'City', 'Area', 
                'Sector', 'Sub Sector', 'Current Partner', 'Current Patner Feedback',
                'Current Patner Feedback Reason', 'Prefered Partners','Implementation Timeline',
                'Meating Timeline', 'L1 Answers','L1 Answer 2', 'L2 Answers','L2 Answer 2', 'Lead Status', 'Comment','Submitted',
                'Call Back Preference']

            book = Workbook()
            sheet = book.active
            sheet.append(header_list)

            
            for row1 in y:
                
                contact_details = None
                if row1['botData']['phone']:
                    contact_details = ContactDetails.objects.filter(
                        Q(mobile=row1['botData']['phone'])|Q(landline=row1['botData']['phone'])).first()

                if row1['botData']['data']:
                    for x in row1['botData']['data']:

                        try:
                            sector_name = x['service']
                        except Exception as e:
                            sector_name = None

                        try:
                            sub_sector_name = x['subService']
                        except Exception as e:
                            sub_sector_name = None

                        try:
                            current_patner = x['existingPartner']
                        except Exception as e:
                            current_patner = None

                        try:
                            current_patner_feedback = x['partnerFeedback']
                        except Exception as e:
                            current_patner_feedback = None

                        try:
                            current_patner_feedback_reason = x['feedbackReason']
                        except Exception as e:
                            current_patner_feedback_reason = None

                        try:
                            prefered_patners = x['preferredPartner']
                        except Exception as e:
                            prefered_patners = None

                        try:
                            implementation_timeline = x['implementationTime']
                        except Exception as e:
                            implementation_timeline = None

                        try:
                            meating_timeline = x['meetingTime']
                        except Exception as e:
                            meating_timeline = None

                        try:
                            l1_answers = x['L1Response_1']
                        except Exception as e:
                            l1_answers = None

                        try:
                            l1_answer_2 = x['L1Response_2']
                        except Exception as e:
                            l1_answer_2 = None

                        try:
                            l1_answer_2 = x['L1Response_2']
                        except Exception as e:
                            l1_answer_2 = None

                        try:
                            l2_answers = x['L2Response_1']
                        except Exception as e:
                            l2_answers = None

                        try:
                            l2_answer_2 = x['L2Response_2']
                        except Exception as e:
                            l2_answer_2 = None

                        try:
                            call_back_preference = x['contactBackTime']
                        except Exception as e:
                            call_back_preference = None

                        supplier_id = ""
                        supplier_type = "RS"
                        sector = None
                        if sector_name is not None:

                            sector = BusinessTypes.objects.filter(
                                business_type=sector_name.lower()).first()
                        
                        sub_sector = None
                        if sub_sector_name is not None:
                            sub_sector = BusinessSubTypes.objects.filter(
                                business_sub_type=sub_sector_name.lower()).first()
                        
                        supplier = None
                        city = None
                        area = None
                        supplier_name = None
                        if contact_details:
                            
                            supplier_id = contact_details.object_id
                            supplier = SupplierTypeSociety.objects.filter(
                                supplier_id=supplier_id).first()
                            if supplier:
                                supplier_name = supplier.society_name
                                city = supplier.society_city
                                area = supplier.society_locality

                            else:
                                supplier = SupplierMaster.objects.filter(
                                    supplier_id=supplier_id).first()

                                if supplier:
                                    supplier_type = supplier.supplier_type
                                    city = supplier.city
                                    area = supplier.area
                                    supplier_name = supplier.supplier_name

                        change_current_patner = "no"
                        if current_patner_feedback == "Dissatisfied" or current_patner_feedback == "Extremely Dissatisfied":
                            change_current_patner = "yes"

                        prefered_patners_array = []
                        if prefered_patners:
                            prefered_patners_split = prefered_patners.split(",")
                            prefered_patners_array = [row.strip() for row in prefered_patners_split]

                        prefered_patners_list = []
                        prefered_patners_id_list = []
                        preferred_company_other = None
                        if prefered_patners_array:
                            prefered_patners_list = Organisation.objects.filter(name__in=prefered_patners_array).all()
                            prefered_patners_id_list = [row.organisation_id for row in prefered_patners_list]
                            prefered_patners_name_list = [row.name for row in prefered_patners_list]

                            if len(prefered_patners_name_list) < len(prefered_patners_array):
                                for prefered_patners_name in prefered_patners_array:
                                    if prefered_patners_name not in prefered_patners_name_list:
                                        preferred_company_other = prefered_patners_name
                                        break

                        lead_status = b2b_utils.get_lead_status(
                            impl_timeline = implementation_timeline,
                            meating_timeline = meating_timeline,
                            company=None,
                            prefered_patners=prefered_patners_list,
                            change_current_patner=change_current_patner.lower()
                            )


                        row2 = [
                            row1['botData']['phone'],
                            supplier_name,
                            city,
                            area,
                            sector_name,
                            sub_sector_name,
                            current_patner,
                            current_patner_feedback,
                            current_patner_feedback_reason,
                            prefered_patners,
                            implementation_timeline,
                            meating_timeline,
                            l1_answers,
                            l1_answer_2,
                            l2_answers,
                            l2_answer_2,
                            lead_status,
                            None,
                            "no",
                            call_back_preference,
                        ]
                        sheet.append(row2)

            resp = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            resp['Content-Disposition'] = 'attachment; filename=mydata.xlsx'
            book.save(resp)
            return resp
        else:
            return ui_utils.handle_response({}, data={
                        "error":"data not found"}, success=False)