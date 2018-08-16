from rest_framework.views import APIView
from openpyxl import load_workbook
from serializers import LeadsSerializer
from models import LeadsForm, LeadsFormItems, LeadsFormData
import v0.ui.utils as ui_utils


class LeadsViewSetExcel(APIView):

    def post(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        leads_list = []
        serializer_list = []
        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
                base_data = {}
                supplier_type_code = row[0].value if row[0].value else None
                base_data = {
                    'supplierCode': supplier_type_code,
                    'object_id': str(row[1].value) if row[1].value else None,
                    'campaign': row[2].value if row[2].value else None
                }
                leads_list.append(base_data)
                response = ui_utils.get_content_type(supplier_type_code)
                if not response:
                    return response
                content_type = response.data.get('data')
                base_data['content_type'] = content_type.id
                base_data['firstname1'] = str(row[3].value) if row[3].value else None
                base_data['lastname1'] = str(row[5].value) if row[5].value else None
                base_data['firstname2'] = str(row[6].value) if row[6].value else None
                base_data['alphanumeric1'] = str(row[4].value) if row[4].value else None
                base_data['lastname2'] = str(row[8].value) if row[8].value else None
                base_data['number1'] = int(row[7].value) if row[7].value else None
                base_data['alphanumeric2'] = str(row[9].value) if row[9].value else None
                base_data['number2'] = int(row[10].value) if row[10].value else None
                base_data['mobile1'] = int(row[11].value) if row[11].value else None
                base_data['mobile2'] = int(row[12].value) if row[12].value else None
                base_data['email1'] = str(row[13].value) if row[13].value else None
                base_data['number2'] = int(row[15].value) if row[15].value else None
                base_data['date1'] = row[14].value.date() if row[14].value else None
                base_data['alphanumeric2'] = str(row[16].value) if row[16].value else None
                base_data['alphanumeric3'] = str(row[17].value) if row[17].value else None
                base_data['is_from_sheet'] = True
                base_data['is_interested'] = row[18].value if row[18].value else False

                serializer = LeadsSerializer(data=base_data)
                if serializer.is_valid():
                    serializer.save()
                    serializer_list.append(serializer.data)
                else:
                    return ui_utils.handle_response(class_name, data=serializer.errors)

        return ui_utils.handle_response(class_name, data=serializer_list, success=True)


class CreateLeadsForm(APIView):

    def post(self, request, campaign_id):
        """
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        leads_form_name = request.data['leads_form_name']
        leads_form_items = request.data['leads_form_items']
        new_dynamic_form = LeadsForm(**{
            'campaign_id': campaign_id,
            'leads_form_name': leads_form_name,
        })
        new_dynamic_form.save()
        form_items_list = []
        item_id = 1
        for item in leads_form_items:
            form_items_list.append(LeadsFormItems(**{
                "leads_form": new_dynamic_form,
                "key_name": item["key_name"],
                "key_type": item["key_type"],
                "key_options": item["key_options"] if "key_options" in item else None,
                "order_id": item["order_id"],
                "item_id": item_id
            }))
            item_id = item_id + 1
        LeadsFormItems.objects.bulk_create(form_items_list)
        return ui_utils.handle_response({}, data='success', success=True)


class GetLeadsForm(APIView):

    def get(self, request, campaign_id):
        """
        :param request:
        :return:
        """
        campaign_lead_form = LeadsForm.objects.filter(campaign_id=campaign_id)
        lead_form_dict = {}
        for lead_from in campaign_lead_form:
            all_items = LeadsFormItems.objects.filter(leads_form_id=lead_from.id)
            lead_form_dict[lead_from.id] = {
                "leads_form_name": lead_from.leads_form_name,
                "leads_form_items": []
            }
            for item in all_items:
                lead_form_dict[lead_from.id]["leads_form_items"].append({
                    "key_name": item.key_name,
                    "key_type": item.key_type,
                    "order_id": item.order_id
                })
        return ui_utils.handle_response({}, data=lead_form_dict, success=True)
