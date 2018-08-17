from rest_framework.views import APIView
from openpyxl import load_workbook, Workbook
from serializers import LeadsSerializer, LeadsFormItemsSerializer
from models import LeadsForm, LeadsFormItems, LeadsFormData
import v0.ui.utils as ui_utils

def enter_lead(TableName, lead_data, supplier_id, lead_form, entry_id):
    form_entry_list = []
    for entry in lead_data:
        form_entry_list.append(TableName(**{
            "supplier_id": supplier_id,
            "item_id": entry["item_id"],
            "item_value": entry["value"],
            "leads_form": lead_form,
            "entry_id": entry_id
        }))
    TableName.objects.bulk_create(form_entry_list)
    lead_form.last_entry_id = entry_id
    lead_form.save()

class GetLeadsEntries(APIView):

    def get(self, request, leads_form_id, supplier_id):
        """
        :param request:
        :return:
        """
        lead_form_items_list = LeadsFormItems.objects.filter(leads_form_id=leads_form_id)
        lead_form_entries_list = LeadsFormData.objects.filter(leads_form_id=leads_form_id)
        all_lead_entries = []
        lead_form_items_dict = {}
        for item in lead_form_items_list:
            lead_form_items_dict[item.item_id] = LeadsFormItemsSerializer(item).data
        for entry in lead_form_entries_list:
            all_lead_entries.append({
                'key_name': lead_form_items_dict[entry.item_id]["key_name"],
                'key_type': lead_form_items_dict[entry.item_id]["key_type"],
                'key_options': lead_form_items_dict[entry.item_id]["key_options"],
                'order_id': lead_form_items_dict[entry.item_id]["order_id"],
                'value': entry.item_value,
            })
        supplier_all_lead_entries = {
            'supplier_id': supplier_id,
            'all_lead_entries': all_lead_entries,
            'total_leads': len(lead_form_entries_list)
        }
        return ui_utils.handle_response({}, data=supplier_all_lead_entries, success=True)

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
                "leads_form_id": lead_from.id,
                "leads_form_items": []
            }
            for item in all_items:
                lead_form_dict[lead_from.id]["leads_form_items"].append({
                    "key_name": item.key_name,
                    "key_type": item.key_type,
                    "order_id": item.order_id
                })
        return ui_utils.handle_response({}, data=lead_form_dict, success=True)


class LeadsFormBulkEntry(APIView):
    def post(self, request, leads_form_id):
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        lead_form = LeadsForm.objects.get(id=leads_form_id)
        entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1

        for index, row in enumerate(ws.iter_rows()):
            form_entry_list = []
            supplier_id = row[0].value if row[0].value else None
            for item_id in range(1, len(row)):
                form_entry_list.append(LeadsFormData(**{
                    "supplier_id": supplier_id,
                    "item_id": item_id,
                    "item_value": row[item_id].value if row[item_id].value else None,
                    "leads_form": lead_form,
                    "entry_id": entry_id
                }))
            LeadsFormData.objects.bulk_create(form_entry_list)
            entry_id = entry_id + 1  # will be saved in the end
        lead_form.last_entry_id = entry_id
        lead_form.save()
        return ui_utils.handle_response({}, data='success', success=True)


class LeadsFormEntry(APIView):
    def post(self, request, leads_form_id):
        """
        :param request:
        :return:
        """
        supplier_id = request.data['supplier_id']
        form_entry_list = []
        lead_form = LeadsForm.objects.get(id=leads_form_id)
        entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1
        lead_data = request.data["leads_form_entries"]
        enter_lead(LeadsFormData, lead_data, supplier_id, lead_form, entry_id)
        return ui_utils.handle_response({}, data='success', success=True)

class GenerateLeadForm(APIView):

    def post(self, request, leads_form_id):
        lead_form_items_list = LeadsFormItems.objects.filter(leads_form_id=leads_form_id)
        lead_form_items_dict = {}
        keys_list = []
        for item in lead_form_items_list:
            curr_row = LeadsFormItemsSerializer(item).data
            lead_form_items_dict[item.item_id] = curr_row
            keys_list.append(curr_row['key_name'])
        book = Workbook()
        sheet = book.active
        sheet.append(keys_list)
        book.save('v0/ui/leads/form_test.xlsx')
        return ui_utils.handle_response({}, data='success', success=True)
