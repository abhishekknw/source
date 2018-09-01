from rest_framework.views import APIView
from openpyxl import load_workbook, Workbook
from serializers import LeadsFormItemsSerializer
from models import LeadsForm, LeadsFormItems, LeadsFormData
import v0.ui.utils as ui_utils
import boto3
import os
import datetime
from django.conf import settings


def enter_lead(lead_data, supplier_id, lead_form, entry_id):
    form_entry_list = []
    for entry in lead_data:
        form_entry_list.append(LeadsFormData(**{
            "supplier_id": supplier_id,
            "item_id": entry["item_id"],
            "item_value": entry["value"],
            "leads_form": lead_form,
            "entry_id": entry_id
        }))
    LeadsFormData.objects.bulk_create(form_entry_list)
    lead_form.last_entry_id = entry_id
    lead_form.save()


class GetLeadsEntries(APIView):
    @staticmethod
    def get(request, leads_form_id, supplier_id):
        lead_form_items_list = LeadsFormItems.objects.filter(leads_form_id=leads_form_id).exclude(status='inactive')
        lead_form_entries_list = LeadsFormData.objects.filter(leads_form_id=leads_form_id).exclude(status='inactive')

        values = []
        lead_form_items_dict = {}
        lead_form_items_dict_part = []
        for item in lead_form_items_list:
            curr_item = LeadsFormItemsSerializer(item).data
            lead_form_items_dict[item.item_id] = curr_item
            curr_item_part = {key:curr_item[key] for key in ['order_id', 'key_name','hot_lead_criteria']}
            lead_form_items_dict_part.append(curr_item_part)

        previous_entry_id = -1
        current_list = []
        hot_leads = []
        counter = 0
        hot_lead = False
        for entry in lead_form_entries_list:
            entry_id = entry.entry_id - 1
            if entry.item_id not in lead_form_items_dict:
                continue
            hot_lead_criteria = lead_form_items_dict[entry.item_id]["hot_lead_criteria"]
            value = entry.item_value
            if value == hot_lead_criteria and hot_lead is False:
                hot_lead = True
                hot_leads.append(counter)
            new_entry = ({
                "order_id": lead_form_items_dict[entry.item_id]["order_id"],
                "value": value,
            })
            if entry_id != previous_entry_id and current_list != []:
                hot_lead = False
                values.append(current_list)
                current_list = []
                counter = counter + 1

            current_list.append(new_entry)
            # values.append([new_entry])

            previous_entry_id = entry_id
        values.append(current_list)

        supplier_all_lead_entries = {
            'supplier_id': supplier_id,
            'headers': lead_form_items_dict_part,
            'values': values,
            'hot_leads': hot_leads
        }
        return ui_utils.handle_response({}, data=supplier_all_lead_entries, success=True)


class CreateLeadsForm(APIView):
    @staticmethod
    def post(request, campaign_id):
        leads_form_name = request.data['leads_form_name']
        leads_form_items = request.data['leads_form_items']
        new_dynamic_form = LeadsForm(**{
            'campaign_id': campaign_id,
            'leads_form_name': leads_form_name,
        })
        new_dynamic_form.save()
        form_items_list = []
        item_id = 0
        for item in leads_form_items:
            item_id = item_id + 1
            item_object = LeadsFormItems(**{
                "leads_form": new_dynamic_form,
                "key_name": item["key_name"],
                "key_type": item["key_type"],
                #"key_options": ",".join(item["key_options"]) if "key_options" in item else None,
                "key_options": item["key_options"] if "key_options" in item else None,
                "order_id": item["order_id"],
                "item_id": item_id,
                "hot_lead_criteria": item["hot_lead_criteria"] if "hot_lead_criteria" in item else None
            })
            form_items_list.append(item_object)
            item_object.save()
        #LeadsFormItems.objects.bulk_create(form_items_list)
        new_dynamic_form.fields_count = item_id
        new_dynamic_form.save()
        return ui_utils.handle_response({}, data='success', success=True)


class GetLeadsForm(APIView):
    @staticmethod
    def get(request, campaign_id):
        campaign_lead_form = LeadsForm.objects.filter(campaign_id=campaign_id).exclude(status='inactive')
        lead_form_dict = {}
        for lead_from in campaign_lead_form:
            all_items = LeadsFormItems.objects.filter(leads_form_id=lead_from.id).exclude(status='inactive')
            lead_form_dict[lead_from.id] = {
                "leads_form_name": lead_from.leads_form_name,
                "leads_form_id": lead_from.id,
                "leads_form_items": []
            }

            for item in all_items:
                lead_form_dict[lead_from.id]["leads_form_items"].append({
                    "key_name": item.key_name,
                    "key_type": item.key_type,
                    "key_options": item.key_options.split(",") if item.key_options else None,
                    "item_id": item.item_id,
                    "order_id": item.order_id,
                    "hot_lead_criteria": item.hot_lead_criteria if item.hot_lead_criteria else None
                })
        return ui_utils.handle_response({}, data=lead_form_dict, success=True)


class LeadsFormBulkEntry(APIView):
    @staticmethod
    def post(request, leads_form_id):
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        lead_form = LeadsForm.objects.get(id=leads_form_id)
        entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1

        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
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
        lead_form.last_entry_id = entry_id-1
        lead_form.save()
        return ui_utils.handle_response({}, data='success', success=True)


class LeadsFormEntry(APIView):
    @staticmethod
    def post(request, leads_form_id):
        supplier_id = request.data['supplier_id']
        form_entry_list = []
        lead_form = LeadsForm.objects.get(id=leads_form_id)
        entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1
        lead_data = request.data["leads_form_entries"]
        enter_lead(lead_data, supplier_id, lead_form, entry_id)
        return ui_utils.handle_response({}, data='success', success=True)


class GenerateLeadForm(APIView):
    @staticmethod
    def get(request, leads_form_id):
        lead_form_items_list = LeadsFormItems.objects.filter(leads_form_id=leads_form_id).exclude(status='inactive')
        lead_form_items_dict = {}
        keys_list = []
        for item in lead_form_items_list:
            curr_row = LeadsFormItemsSerializer(item).data
            lead_form_items_dict[item.item_id] = curr_row
            keys_list.append(curr_row['key_name'])
        book = Workbook()
        sheet = book.active
        sheet.append(keys_list)
        now = datetime.datetime.now()
        current_date = now.strftime("%d%m%Y_%H%M")
        cwd = os.path.dirname(os.path.realpath(__file__))
        filename = 'leads_form_' + current_date + '.xlsx'
        filepath = cwd + '/' + filename
        book.save(filepath)

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        with open(filepath) as f:
            try:
                s3.put_object(Body=f, Bucket='leads-forms-templates', Key=filename)
                os.unlink(filepath)
            except Exception as ex:
                print ex
        return ui_utils.handle_response({}, data={'filepath': 'https://s3.ap-south-1.amazonaws.com/leads-forms-templates/' + filename}, success=True)


class DeleteLeadItems(APIView):
    # Items are marked inactive, while still present in DB
    @staticmethod
    def put (request, form_id, item_id):
        lead_form_item = LeadsFormItems.objects.get(leads_form_id=form_id, item_id=item_id)
        lead_form_item.status = 'inactive'
        lead_form_item.save()
        return ui_utils.handle_response({}, data='success', success=True)


class DeleteLeadForm(APIView):
    # Entire form is deactivated
    @staticmethod
    def put(request, form_id):
        form_details = LeadsForm.objects.get(id=form_id)
        form_details.status = 'inactive'
        form_details.save()
        return ui_utils.handle_response({}, data='success', success=True)


class DeleteLeadEntry(APIView):
    @staticmethod
    def put(request, form_id, entry_id):
        entry_list = LeadsFormData.objects.filter(leads_form_id=form_id, entry_id=entry_id)
        for items in entry_list:
            items.status = 'inactive'
            items.save()
        return ui_utils.handle_response({}, data='success', success=True)


class LeadFormUpdate(APIView):
    # this function is used to add fields to an existing form using form id
    @staticmethod
    def put(request, form_id):
        new_field = request.data
        new_field_object = LeadsFormItems(**new_field)
        new_field_object.leads_form_id = form_id
        last_item_id = LeadsForm.objects.get(id=form_id).fields_count
        new_field_object.item_id = last_item_id + 1
        new_field_object.save()
        return ui_utils.handle_response({}, data='success', success=True)


# class ImportCampaignLeads(APIView):
#     """
#     DEPRECATED
#     The api to import campaign leads data
#     """
#
#     def post(self, request):
#         class_name = self.__class__.__name__
#         if not request.FILES:
#             return ui_utils.handle_response(class_name, data='No File Found')
#         my_file = request.FILES['file']
#         wb = openpyxl.load_workbook(my_file)
#
#         ws = wb.get_sheet_by_name('campaign_leads')
#
#         result = []
#
#         try:
#             # iterate through all rows and populate result array
#             for index, row in enumerate(ws.iter_rows()):
#                 if index == 0:
#                     continue
#
#                 # make a dict of the row
#                 row_response = website_utils.get_mapped_row(ws, row)
#                 if not row_response.data['status']:
#                     return row_response
#                 row = row_response.data['data']
#
#                 # handle it
#                 response = website_utils.handle_campaign_leads(row)
#                 if not response.data['status']:
#                     return response
#
#                 result.append(response.data['data'])
#             return ui_utils.handle_response(class_name, data=result, success=True)
#         except Exception as e:
#             return ui_utils.handle_response(class_name, exception_object=e, request=request)
