from rest_framework.views import APIView
from openpyxl import load_workbook, Workbook
from serializers import LeadsFormItemsSerializer, LeadsFormContactsSerializer
from models import LeadsForm, LeadsFormItems, LeadsFormData, LeadsFormContacts, LeadsFormSummary
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.inventory.models import (InventoryActivityAssignment, InventoryActivity)
from v0.ui.campaign.views import (lead_counter, get_leads_data_for_campaign,
                                  get_leads_data_for_multiple_campaigns)
import v0.ui.utils as ui_utils
from v0.ui.utils import calculate_percentage
import boto3
import os
import datetime
from django.conf import settings
from bulk_update.helper import bulk_update
from v0.ui.common.models import BaseUser
from v0.ui.campaign.models import CampaignAssignment
from v0.constants import campaign_status, proposal_on_hold
from django.http import HttpResponse
from celery import shared_task


def enter_lead(lead_data, supplier_id, campaign_id, lead_form, entry_id):
    form_entry_list = []
    for entry in lead_data:
        form_entry_list.append(LeadsFormData(**{
            "supplier_id": supplier_id,
            "campaign_id": campaign_id,
            "item_id": entry["item_id"],
            "item_value": entry["value"] if 'value' in entry else None,
            "leads_form": lead_form,
            "entry_id": entry_id,
            "created_at": datetime.datetime.now()
        }))
    LeadsFormData.objects.bulk_create(form_entry_list)
    lead_form.last_entry_id = entry_id
    lead_form.save()


def get_supplier_all_leads_entries(leads_form_id, supplier_id,page_number=0, **kwargs):
    leads_per_page=25
    lead_form_items_list = LeadsFormItems.objects.filter(leads_form_id=leads_form_id).exclude(status='inactive')
    if supplier_id == 'All':
        lead_form_entries_list = LeadsFormData.objects.filter(leads_form_id=leads_form_id).exclude(
            status='inactive')
        suppliers_list = lead_form_entries_list.values_list('supplier_id',flat=True)
        suppliers_names = SupplierTypeSociety.objects.filter(supplier_id__in=suppliers_list).values_list(
            'supplier_id','society_name')
        supplier_id_names = dict((x,y) for x,y in suppliers_names)
    else:
        lead_form_entries_list = LeadsFormData.objects.filter(leads_form_id=leads_form_id) \
            .filter(supplier_id=supplier_id).exclude(status='inactive')
        supplier_data = SupplierTypeSociety.objects.get(supplier_id=supplier_id)
        supplier_name = supplier_data.society_name
    if 'start_date' in kwargs and kwargs['start_date']:
        lead_form_entries_list = lead_form_entries_list.filter(created_at__gte=kwargs['start_date'])

    if 'end_date' in kwargs and kwargs['end_date']:
        lead_form_entries_list = lead_form_entries_list.filter(created_at__lte=kwargs['end_date'])
    values = []
    lead_form_items_dict = {}
    lead_form_items_dict_part = []
    for item in lead_form_items_list:
        curr_item = LeadsFormItemsSerializer(item).data
        lead_form_items_dict[item.item_id] = curr_item
        curr_item_part = {key: curr_item[key] for key in ['order_id', 'key_name', 'hot_lead_criteria']}
        lead_form_items_dict_part.append(curr_item_part)
    lead_form_items_dict_part.insert(0, {
        'order_id': 0,
        'key_name': 'Lead Date'
    })
    lead_form_items_dict_part.insert(0,{
        'order_id': 0,
        'key_name': 'Supplier Name'
    })


    previous_entry_id = -1
    current_list = []
    hot_leads = []
    counter = 1
    if page_number>0:
        min_counter = leads_per_page*(page_number-1)+1
        max_counter = leads_per_page*page_number
        lead_form_entries_list = lead_form_entries_list.filter(entry_id__gte=min_counter).filter(entry_id__lte=max_counter)

    entry_id = None
    for entry in lead_form_entries_list:
        curr_item_id = entry.item_id
        if curr_item_id not in lead_form_items_dict:
            continue
        curr_item = lead_form_items_dict[curr_item_id]
        hot_lead_criteria = curr_item["hot_lead_criteria"]
        value = entry.item_value
        entry_id = entry.entry_id
        if value and (value == hot_lead_criteria or 'counseling' in curr_item['key_name'].lower()):
            if entry_id not in hot_leads:
                hot_leads.append(entry_id)
        new_entry = ({
            "order_id": curr_item["order_id"],
            "value": value,
        })
        if entry_id != previous_entry_id and current_list != []:
            if supplier_id == 'All':
                curr_supplier_id = entry.supplier_id
                curr_supplier_name = supplier_id_names[curr_supplier_id]
            else:
                curr_supplier_name = supplier_name
            current_list.insert(0, {
                "order_id": 0,
                "value": entry.created_at,
            })
            current_list.insert(0, {
                "order_id": 0,
                "value": curr_supplier_name,
            })
            values.append(current_list)
            current_list = []
            counter = counter + 1

        current_list.append(new_entry)
        previous_entry_id = entry_id
    values.append(current_list)

    supplier_all_lead_entries = {
        'headers': lead_form_items_dict_part,
        'values': values,
        'hot_leads': hot_leads
    }
    if not supplier_id == 'All':
        supplier_all_lead_entries.append(
            {"order_id": 0,
             "value": supplier_id})
        supplier_all_lead_entries.append(
            {"order_id": 0,
             "value": supplier_name})
    return supplier_all_lead_entries


class GetLeadsEntries(APIView):
    @staticmethod
    def get(request, leads_form_id):
        supplier_id = request.query_params.get('supplier_id','All')

        page_number = int(request.query_params.get('page_number',0))
        supplier_all_lead_entries = get_supplier_all_leads_entries(leads_form_id, supplier_id,page_number)
        return ui_utils.handle_response({}, data=supplier_all_lead_entries, success=True)


class GetLeadsEntriesByCampaignId(APIView):
    # it is assumed that a form belongs to a campaign
    @staticmethod
    def get(request, campaign_id, supplier_id='All'):
        page_number = int(request.query_params.get('page_number', 0))
        first_leads_form_id = LeadsForm.objects.filter(campaign_id=campaign_id).all()[0].id
        supplier_all_lead_entries = get_supplier_all_leads_entries(first_leads_form_id, supplier_id, page_number)
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
            key_options = item["key_options"] if 'key_options' in item else None
            if key_options and isinstance(key_options, list):
                key_options = ','.join(key_options)
            item_object = LeadsFormItems(**{
                "campaign_id": campaign_id,
                "leads_form": new_dynamic_form,
                "key_name": item["key_name"],
                "key_type": item["key_type"],
                "key_options": key_options,
                "order_id": item["order_id"],
                "item_id": item_id,
                "hot_lead_criteria": item["hot_lead_criteria"] if "hot_lead_criteria" in item else None
            })
            form_items_list.append(item_object)
            item_object.save()
        # LeadsFormItems.objects.bulk_create(form_items_list)
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
        fields = lead_form.fields_count
        campaign_id = lead_form.campaign_id
        entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1
        missing_societies = []
        inv_activity_assignment_missing_societies = []
        inv_activity_missing_societies = []
        not_present_in_shortlisted_societies = []
        more_than_ones_same_shortlisted_society = []
        unresolved_societies = []
        for index, row in enumerate(ws.iter_rows()):
            if index == 0:
                for idx, i in enumerate(row):
                    if 'apartment' in i.value.lower():
                        apartment_index = idx
                        break
            if index > 0:
                form_entry_list = []
                # supplier_id = row[0].value if row[0].value else None
                # created_at = row[1].value if row[1].value else None
                society_name = row[apartment_index].value
                suppliers = SupplierTypeSociety.objects.filter(society_name=society_name).values('supplier_id',
                                                                                                 'society_name').all()
                if len(suppliers) == 0:
                    if society_name not in missing_societies:
                        missing_societies.append(society_name)
                    continue
                else:
                    if len(suppliers) == 1:
                        found_supplier_id = suppliers[0]['supplier_id']
                    else:
                        supplier_ids = []
                        for s in suppliers:
                            supplier_ids.append(s['supplier_id'])
                        shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id,
                                                                              object_id__in=supplier_ids).values(
                            'object_id', 'id').all()
                        if len(shortlisted_spaces) > 1:
                            more_than_ones_same_shortlisted_society.append(society_name)
                            continue
                        if len(shortlisted_spaces) == 0:
                            not_present_in_shortlisted_societies.append(society_name)
                            continue
                        else:
                            found_supplier_id = shortlisted_spaces[0]['object_id']
                shortlisted_spaces = ShortlistedSpaces.objects.filter(object_id=found_supplier_id).filter(
                    proposal_id=campaign_id).all()
                if len(shortlisted_spaces) == 0:
                    not_present_in_shortlisted_societies.append(society_name)
                    continue
                inventory_list = ShortlistedInventoryPricingDetails.objects.filter(
                    shortlisted_spaces_id=shortlisted_spaces[0].id).all()
                stall = None
                for inventory in inventory_list:
                    if inventory.ad_inventory_type_id >= 8 and inventory.ad_inventory_type_id <= 11:
                        stall = inventory
                        break
                if not stall:
                    continue
                shortlisted_inventory_details_id = stall.id
                inventory_list = InventoryActivity.objects.filter(
                    shortlisted_inventory_details_id=shortlisted_inventory_details_id, activity_type='RELEASE').all()
                if len(inventory_list) == 0:
                    inv_activity_missing_societies.append(society_name)
                    continue
                inventory_activity_id = inventory_list[0].id
                inventory_activity_list = InventoryActivityAssignment.objects.filter(
                    inventory_activity_id=inventory_activity_id).all()
                if len(inventory_activity_list) == 0:
                    inv_activity_assignment_missing_societies.append(society_name)
                    continue

                created_at = inventory_activity_list[0].activity_date
                for item_id in range(0, fields):
                    form_entry_list.append(LeadsFormData(**{
                        "campaign_id": campaign_id,
                        "supplier_id": found_supplier_id,
                        "item_id": item_id + 1,
                        "item_value": row[item_id].value if row[item_id].value else None,
                        "leads_form": lead_form,
                        "entry_id": entry_id,
                        "created_at": created_at
                    }))
                LeadsFormData.objects.bulk_create(form_entry_list)
                entry_id = entry_id + 1  # will be saved in the end
        recreate_leads_summary.delay()
        get_leads_data_for_campaign.delay(campaign_id, None, None, True)
        get_leads_data_for_multiple_campaigns.delay([campaign_id], True)
        lead_form.last_entry_id = entry_id - 1
        lead_form.save()
        missing_societies.sort()
        print "missing societies", missing_societies
        print "unresolved_societies", list(set(unresolved_societies))
        print "more_than_ones_same_shortlisted_society", list(set(more_than_ones_same_shortlisted_society))
        print "inv_activity_assignment_missing_societies", list(set(inv_activity_assignment_missing_societies))
        print "inv_activit_missing_societies", list(set(inv_activity_missing_societies))
        print "not_present_in_shortlisted_societies", list(set(not_present_in_shortlisted_societies))
        return ui_utils.handle_response({}, data='success', success=True)


# class LeadsFormBulkEntryOriginal(APIView):
#     @staticmethod
#     def post(request, leads_form_id):
#         source_file = request.data['file']
#         wb = load_workbook(source_file)
#         ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
#         lead_form = LeadsForm.objects.get(id=leads_form_id)
#         fields = lead_form.fields_count
#         campaign_id = lead_form.campaign_id
#         entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1
#
#         for index, row in enumerate(ws.iter_rows()):
#             if index > 0:
#                 form_entry_list = []
#                 supplier_id = row[0].value if row[0].value else None
#                 created_at = row[1].value if row[1].value else None
#                 for index, row in enumerate(ws.iter_rows()):
#                     if index > 0:
#                         form_entry_list = []
#                         supplier_id = row[0].value if row[0].value else None
#                         created_at = row[1].value if row[1].value else None
#                         for item_id in range(2, fields + 1):
#                             form_entry_list.append(LeadsFormData(**{
#                                 "campaign_id": campaign_id,
#                                 "supplier_id": supplier_id,
#                                 "item_id": item_id - 1,
#                                 "item_value": row[item_id].value if row[item_id].value else None,
#                                 "leads_form": lead_form,
#                                 "entry_id": entry_id,
#                                 "created_at": created_at
#                             }))
#                         LeadsFormData.objects.bulk_create(form_entry_list)
#                         entry_id = entry_id + 1  # will be saved in the end
#                 lead_form.last_entry_id = entry_id - 1
#                 lead_form.save()
#         lead_form.last_entry_id = entry_id-1
#         lead_form.save()
#         return ui_utils.handle_response({}, data='success', success=True)


class LeadsFormEntry(APIView):
    @staticmethod
    def post(request, leads_form_id):
        supplier_id = request.data['supplier_id']
        form_entry_list = []
        lead_form = LeadsForm.objects.get(id=leads_form_id)
        entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1
        campaign_id = lead_form.campaign_id
        lead_data = request.data["leads_form_entries"]
        enter_lead(lead_data, supplier_id, campaign_id, lead_form, entry_id)
        lead_form_items_list = LeadsFormItems.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
        lead_count = lead_counter(campaign_id, supplier_id, lead_form_items_list)
        hot_lead_percentage = calculate_percentage(lead_count['hot_leads'], lead_count['total_leads'])
        LeadsFormSummary.objects.update_or_create(leads_form_id=leads_form_id, supplier_id=supplier_id, defaults={
            'leads_form': lead_form,
            'campaign_id': campaign_id,
            'supplier_id': supplier_id,
            'hot_leads_count': lead_count['hot_leads'],
            'total_leads_count': lead_count['total_leads'],
            'hot_leads_percentage': hot_lead_percentage
        })
        return ui_utils.handle_response({}, data='success', success=True)

@shared_task()
def recreate_leads_summary():
    all_leads_form = LeadsForm.objects.all()
    for leads_form in all_leads_form:
        leads_form_id = leads_form.id
        lead_form = LeadsForm.objects.get(id=leads_form_id)
        campaign_id = leads_form.campaign_id
        shortlisted_suppliers = LeadsFormData.objects.filter(campaign_id=campaign_id).values('supplier_id').distinct()
        shortlisted_suppliers_id_list = [supplier['supplier_id'] for supplier in shortlisted_suppliers]
        for supplier_id in shortlisted_suppliers_id_list:
            lead_form_items_list = LeadsFormItems.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
            lead_count = lead_counter(campaign_id, supplier_id, lead_form_items_list)
            hot_lead_percentage = calculate_percentage(lead_count['hot_leads'], lead_count['total_leads'])
            LeadsFormSummary.objects.update_or_create(leads_form_id=leads_form_id, supplier_id=supplier_id, defaults={
                'leads_form': lead_form,
                'campaign_id': campaign_id,
                'supplier_id': supplier_id,
                'hot_leads_count': lead_count['hot_leads'],
                'total_leads_count': lead_count['total_leads'],
                'hot_leads_percentage': hot_lead_percentage
            })
    return


class MigrateLeadsSummary(APIView):
    def put(self, request):
        class_name = self.__class__.__name__
        recreate_leads_summary.delay()
        return ui_utils.handle_response({}, data='success', success=True)


class GenerateLeadForm(APIView):
    @staticmethod
    def get(request, leads_form_id):
        lead_form_items_list = LeadsFormItems.objects.filter(leads_form_id=leads_form_id).exclude(status='inactive')
        lead_form_items_dict = {}
        keys_list = ['supplier_id', 'lead_entry_date (format: dd/mm/yyyy)']
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
        return ui_utils.handle_response({}, data={
            'filepath': 'https://s3.ap-south-1.amazonaws.com/leads-forms-templates/' + filename}, success=True)


def get_leads_excel_sheet(leads_form_id, supplier_id,**kwargs):
    start_date = kwargs['start_date'] if 'start_date' in kwargs else None
    end_date = kwargs['end_date'] if 'end_date' in kwargs else None
    all_leads = get_supplier_all_leads_entries(leads_form_id, supplier_id, start_date=start_date, end_date=end_date)
    keys_list = []
    for item in all_leads['headers']:
        keys_list.append(item['key_name'])

    book = Workbook()
    sheet = book.active
    sheet.append(keys_list)
    total_leads_count = 0
    for lead in all_leads["values"]:
        value_list = []
        for item_dict in lead:
            if isinstance(item_dict["value"], basestring):
                item_dict["value"] = item_dict["value"].encode("utf8")
            value_list.append(str(item_dict["value"]))
        sheet.append(value_list)
        if value_list != []:
            total_leads_count += 1
    return (book, total_leads_count)


class GenerateLeadDataExcel(APIView):
    @staticmethod
    def get(request, leads_form_id):
        supplier_id = request.GET.get('supplier_id', 'ALL')
        (excel_book, total_leads_count) = get_leads_excel_sheet(leads_form_id, supplier_id)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=mydata.xlsx'

        excel_book.save(response)
        return response



class DeleteLeadItems(APIView):
    # Items are marked inactive, while still present in DB
    @staticmethod
    def put(request, form_id, item_id):
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
        new_field_list = request.data
        lead_form = LeadsForm.objects.get(id=form_id)
        for new_field in new_field_list:
            if 'key_options' in new_field:
                if new_field['key_options'] and isinstance(new_field['key_options'], list):
                    new_field['key_options'] = ','.join(new_field['key_options'])
            new_field_object = LeadsFormItems(**new_field)
            new_field_object.leads_form_id = form_id
            last_item_id = LeadsForm.objects.get(id=form_id).fields_count
            new_field_object.item_id = last_item_id + 1
            new_field_object.campaign_id = lead_form.campaign_id
            new_field_object.save()
        leads_form_items_count = LeadsFormItems.objects.filter(leads_form_id=form_id).count()
        lead_form.fields_count = leads_form_items_count
        lead_form.save()
        return ui_utils.handle_response({}, data='success', success=True)


class EditLeadsData(APIView):
    def put(self, request, form_id):
        class_name = self.__class__.__name__
        form_data = request.data
        leads_form_edit_data = []
        entries = form_data.keys()
        full_query = LeadsFormData.objects.filter(leads_form_id=form_id).filter(entry_id__in=entries).all()
        form_data_complete = []
        for entry_id in entries:
            entry_data = form_data[entry_id]
            items = entry_data.keys()
            for item_id in items:
                form_query = full_query.get(entry_id=entry_id, item_id=item_id)
                form_query.item_value = entry_data[item_id]
                form_data_complete.append(form_query)
        bulk_update(form_data_complete)
        return ui_utils.handle_response(class_name, data='success', success=True)


class EditLeadFormItems(APIView):
    # this function is used to add or edit lead form items
    # if edited, lead form items are removed from the table forever
    def put(self, request, form_id):
        class_name = self.__class__.__name__
        items_dict = request.data
        full_query = LeadsFormItems.objects.filter(leads_form_id=form_id).all()
        items_array = []
        item_ids = items_dict.keys()
        for item_id in item_ids:
            key_name = items_dict[item_id]["Name"]
            key_type = items_dict[item_id]["Type"]
            form_query = full_query.get(item_id=item_id)
            form_query.key_name = key_name
            form_query.key_type = key_type
            items_array.append(form_query)
        bulk_update(items_array)
        return ui_utils.handle_response(class_name, data='success', success=True)


class EditLeadsForm(APIView):
    # For now, only name can be edited
    def put(self, request, form_id):
        class_name = self.__class__.__name__
        name = request.data
        form_query = LeadsForm.objects.get(id=form_id)
        form_query.leads_form_name = name
        form_query.save()
        return ui_utils.handle_response(class_name, data='success', success=True)


class LeadsSummary(APIView):

    def get(self, request):
        class_name = self.__class__.__name__
        username = request.user
        user_id = BaseUser.objects.get(username=username).id
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=user_id).values_list('campaign_id', flat=True).distinct()
        all_shortlisted_supplier = ShortlistedSpaces.objects.filter(proposal_id__in=campaign_list).values('proposal_id',
                                                                                                          'object_id',
                                                                                                          'phase_no_id',
                                                                                                          'is_completed',
                                                                                                          'proposal__name',
                                                                                                          'proposal__tentative_start_date',
                                                                                                          'proposal__tentative_end_date',
                                                                                                          'proposal__campaign_state')
        all_campaign_dict = {}
        all_shortlisted_supplier_id = [supplier['object_id'] for supplier in all_shortlisted_supplier]
        all_supplier_society = SupplierTypeSociety.objects.filter(supplier_id__in=all_shortlisted_supplier_id).values('supplier_id', 'flat_count')
        all_supplier_society_dict = {}
        current_date = datetime.datetime.now().date()
        for supplier in all_supplier_society:
            all_supplier_society_dict[supplier['supplier_id']] = {'flat_count': supplier['flat_count']}
        for shortlisted_supplier in all_shortlisted_supplier:
            if shortlisted_supplier['proposal_id'] not in all_campaign_dict:
                all_campaign_dict[shortlisted_supplier['proposal_id']] = {
                'all_supplier_ids': [], 'all_phase_ids': [], 'total_flat_counts': 0, 'total_leads':0, 'hot_leads':0}
            if shortlisted_supplier['object_id'] not in all_campaign_dict[shortlisted_supplier['proposal_id']]['all_supplier_ids']:
                all_campaign_dict[shortlisted_supplier['proposal_id']]['all_supplier_ids'].append(shortlisted_supplier['object_id'])
                if shortlisted_supplier['object_id'] in all_supplier_society_dict and all_supplier_society_dict[shortlisted_supplier['object_id']]['flat_count']:
                    all_campaign_dict[shortlisted_supplier['proposal_id']]['total_flat_counts'] += all_supplier_society_dict[shortlisted_supplier['object_id']]['flat_count']
            if shortlisted_supplier['phase_no_id'] and shortlisted_supplier['phase_no_id'] not in all_campaign_dict[shortlisted_supplier['proposal_id']]['all_phase_ids']:
                if shortlisted_supplier['proposal__tentative_end_date'].date() < current_date:
                    all_campaign_dict[shortlisted_supplier['proposal_id']]['all_phase_ids'].append(
                        shortlisted_supplier['phase_no_id'])
            all_campaign_dict[shortlisted_supplier['proposal_id']]['name'] = shortlisted_supplier['proposal__name']
            all_campaign_dict[shortlisted_supplier['proposal_id']]['start_date'] = shortlisted_supplier['proposal__tentative_start_date']
            all_campaign_dict[shortlisted_supplier['proposal_id']]['end_date'] = shortlisted_supplier['proposal__tentative_end_date']
            all_campaign_dict[shortlisted_supplier['proposal_id']]['campaign_status'] = shortlisted_supplier['proposal__campaign_state']

        all_campaign_summary = LeadsFormSummary.objects.filter(campaign_id__in=campaign_list).values(
            'supplier_id', 'campaign_id', 'total_leads_count', 'hot_leads_count', 'campaign_id')
        all_leads_summary = []
        for campaign_summary in all_campaign_summary:
            all_campaign_dict[campaign_summary['campaign_id']]['hot_leads'] += campaign_summary['hot_leads_count']
            all_campaign_dict[campaign_summary['campaign_id']]['total_leads'] += campaign_summary['total_leads_count']
        for campaign_id in all_campaign_dict:
            this_campaign_status = None
            if not all_campaign_dict[campaign_id]['campaign_status'] == proposal_on_hold:
                if all_campaign_dict[campaign_id]['start_date'].date() > current_date:
                    this_campaign_status = campaign_status['upcoming_campaigns']
                elif all_campaign_dict[campaign_id]['end_date'].date() >= current_date:
                    this_campaign_status = campaign_status['ongoing_campaigns']
                elif all_campaign_dict[campaign_id]['end_date'].date() < current_date:
                    this_campaign_status = campaign_status['completed_campaigns']
            else:
                this_campaign_status = "on_hold"
            all_leads_summary.append({
                "campaign_id": campaign_id,
                "name": all_campaign_dict[campaign_id]['name'],
                "start_date": all_campaign_dict[campaign_id]['start_date'],
                "end_date": all_campaign_dict[campaign_id]['end_date'],
                "phase_complete": len(all_campaign_dict[campaign_id]['all_phase_ids']),
                "supplier_count": len(all_campaign_dict[campaign_id]['all_supplier_ids']),
                "flat_count": all_campaign_dict[campaign_id]['total_flat_counts'],
                "total_leads": all_campaign_dict[campaign_id]['total_leads'],
                "hot_leads": all_campaign_dict[campaign_id]['hot_leads'],
                "campaign_status": this_campaign_status
            })
        return ui_utils.handle_response(class_name, data=all_leads_summary, success=True)


class SmsContact(APIView):

    def post(self, request, form_id):
        class_name = self.__class__.__name__
        contact_details = request.data
        contact_mobile = contact_details['mobile']
        data = (LeadsFormContacts(**{
            'contact_name': contact_details['name'],
            'contact_mobile': contact_details['mobile'],
            'form_id': form_id
        }))
        data.save()
        return ui_utils.handle_response(class_name, data='success', success=True)

    def get(self, request, form_id):
        class_name = self.__class__.__name__
        contacts_data_object = LeadsFormContacts.objects.filter(form_id=form_id).values('contact_name',
                                                                                        'contact_mobile')
        contacts_data = []
        for data in contacts_data_object:
            contacts_data.append(data)
        return ui_utils.handle_response(class_name, data=contacts_data, success=True)


@shared_task()
def cache_all_campaign_leads():
    all_leads_forms = LeadsForm.objects.all()
    recreate_leads_summary.delay()
    for leads_form in all_leads_forms:
        campaign_id = leads_form.campaign_id
        get_leads_data_for_campaign.delay(campaign_id, None, None, True)
        get_leads_data_for_multiple_campaigns.delay([campaign_id], True)
    return


class CampaignLeadsCacheAll(APIView):
    def get(self, request):
        class_name = self.__class__.__name__
        cache_all_campaign_leads.delay()
        return ui_utils.handle_response(class_name, data={"status": "success"}, success=True)