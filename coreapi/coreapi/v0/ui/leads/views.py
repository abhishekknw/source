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
                    "key_options": item.key_options,
                    "item_id": item.item_id,
                    "order_id": item.order_id
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
        lead_form.last_entry_id = entry_id
        lead_form.save()
        return ui_utils.handle_response({}, data='success', success=True)


class LeadsFormEntry(APIView):
    @staticmethod
    def post(request, leads_form_id):
        supplier_id = request.data['supplier_id']
        form_entry_list = []
        lead_form = LeadsForm.objects.get(id=leads_form_id).exclude(status='inactive')
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


