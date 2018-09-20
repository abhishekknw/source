from rest_framework.views import APIView
from openpyxl import load_workbook, Workbook
from serializers import LeadsFormItemsSerializer, LeadsFormContactsSerializer
from models import LeadsForm, LeadsFormItems, LeadsFormData, Leads, LeadAlias, LeadsFormContacts
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.inventory.models import (InventoryActivityAssignment, InventoryActivity)

import v0.ui.utils as ui_utils
import boto3
import os
import datetime
from django.conf import settings


def enter_lead(lead_data, supplier_id, campaign_id, lead_form, entry_id):
    form_entry_list = []
    for entry in lead_data:
        form_entry_list.append(LeadsFormData(**{
            "supplier_id": supplier_id,
            "campaign_id": campaign_id,
            "item_id": entry["item_id"],
            "item_value": entry["value"],
            "leads_form": lead_form,
            "entry_id": entry_id,
            "created_at": datetime.datetime.now()
        }))
    LeadsFormData.objects.bulk_create(form_entry_list)
    lead_form.last_entry_id = entry_id
    lead_form.save()


class GetLeadsEntries(APIView):
    @staticmethod
    def get(request, leads_form_id, supplier_id = 'All'):
        lead_form_items_list = LeadsFormItems.objects.filter(leads_form_id=leads_form_id).exclude(status='inactive')
        if supplier_id == 'All':
            lead_form_entries_list = LeadsFormData.objects.filter(leads_form_id=leads_form_id). exclude(status='inactive')
        else:
            lead_form_entries_list = LeadsFormData.objects.filter(leads_form_id=leads_form_id)\
                .filter(supplier_id = supplier_id).exclude(status='inactive')

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
        counter = 1
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
        if supplier_id == 'All':
            supplier_all_lead_entries.pop('supplier_id')
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
                "campaign_id" : campaign_id,
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
                suppliers = SupplierTypeSociety.objects.filter(society_name=society_name).values('supplier_id', 'society_name').all()
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
                        shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id, object_id__in=supplier_ids).values('object_id', 'id').all()
                        if len(shortlisted_spaces) > 1:
                            more_than_ones_same_shortlisted_society.append(society_name)
                            continue
                        if len(shortlisted_spaces) == 0:
                            not_present_in_shortlisted_societies.append(society_name)
                            continue
                        else:
                            found_supplier_id = shortlisted_spaces[0]['object_id']
                shortlisted_spaces = ShortlistedSpaces.objects.filter(object_id=found_supplier_id).filter(proposal_id=campaign_id).all()
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
                inventory_list = InventoryActivity.objects.filter(shortlisted_inventory_details_id=shortlisted_inventory_details_id, activity_type='RELEASE').all()
                if len(inventory_list) == 0:
                    inv_activity_missing_societies.append(society_name)
                    continue
                inventory_activity_id = inventory_list[0].id
                inventory_activity_list = InventoryActivityAssignment.objects.filter(inventory_activity_id=inventory_activity_id).all()
                if len(inventory_activity_list) == 0:
                    inv_activity_assignment_missing_societies.append(society_name)
                    continue

                created_at = inventory_activity_list[0].activity_date
                for item_id in range(0, fields):
                    form_entry_list.append(LeadsFormData(**{
                        "campaign_id": campaign_id,
                        "supplier_id": found_supplier_id,
                        "item_id": item_id+1,
                        "item_value": row[item_id].value if row[item_id].value else None,
                        "leads_form": lead_form,
                        "entry_id": entry_id,
                        "created_at": created_at
                    }))
                LeadsFormData.objects.bulk_create(form_entry_list)
                entry_id = entry_id + 1  # will be saved in the end
        lead_form.last_entry_id = entry_id-1
        lead_form.save()
        missing_societies.sort()
        print "missing societies", missing_societies
        print "unresolved_societies", list(set(unresolved_societies))
        print "more_than_ones_same_shortlisted_society", list(set(more_than_ones_same_shortlisted_society))
        print "inv_activity_assignment_missing_societies", list(set(inv_activity_assignment_missing_societies))
        print "inv_activit_missing_societies", list(set(inv_activity_missing_societies))
        print "not_present_in_shortlisted_societies", list(set(not_present_in_shortlisted_societies))
        return ui_utils.handle_response({}, data='success', success=True)


class LeadsFormBulkEntryOriginal(APIView):
    @staticmethod
    def post(request, leads_form_id):
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        lead_form = LeadsForm.objects.get(id=leads_form_id)
        fields = lead_form.fields_count
        campaign_id = lead_form.campaign_id
        entry_id = lead_form.last_entry_id + 1 if lead_form.last_entry_id else 1

        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
                form_entry_list = []
                supplier_id = row[0].value if row[0].value else None
                created_at = row[1].value if row[1].value else None
                for item_id in range(2, fields+1):
                    form_entry_list.append(LeadsFormData(**{
                        "campaign_id": campaign_id,
                        "supplier_id": supplier_id,
                        "item_id": item_id - 1,
                        "item_value": row[item_id].value if row[item_id].value else None,
                        "leads_form": lead_form,
                        "entry_id": entry_id,
                        "created_at": created_at
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
        campaign_id = lead_form.campaign_id
        lead_data = request.data["leads_form_entries"]
        enter_lead(lead_data, supplier_id, campaign_id, lead_form, entry_id)
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


def save_items (fields_dict, fixed_fields,form, current_form_id, entry_id):
    campaign_id = form["campaign_id"]
    supplier_id = form["object_id"]
    items = []
    data = []
    alias_data_object = LeadAlias.objects.filter(campaign_id = campaign_id)
    leads_old_object = Leads.objects.filter(campaign_id = campaign_id, object_id = supplier_id)
    order_id = 0
    for curr_row in alias_data_object:
        original_name = curr_row.original_name
        order_id = order_id + 1
        curr_element = {
             'key_name': curr_row.alias,
             'key_type': fields_dict[original_name],
             'order_id': order_id,
             'item_id': order_id,
             'leads_form_id': current_form_id,
             'campaign_id': campaign_id,
             'supplier_id': supplier_id,
        }
        if original_name=='is_interested':
            curr_element['hot_lead_criteria']=True
        items.append(LeadsFormItems(**curr_element))
        current_entry_id = 1
        for lead in leads_old_object:
            col_value = getattr(lead, original_name)
            if col_value is not None:
                data.append(LeadsFormData(**{
                    'supplier_id': supplier_id,
                    'campaign_id': campaign_id,
                    'item_id': order_id,
                    'item_value': col_value,
                    'leads_form_id': current_form_id,
                    'entry_id': current_entry_id,
                    'created_at': lead.created_at,
                    'updated_at': lead.updated_at
                    }))
            current_entry_id = current_entry_id + 1

    for field in fixed_fields:
        order_id = order_id + 1
        added_fields = {
            'order_id': order_id,
            'item_id': order_id,
            'leads_form_id': current_form_id,
            'campaign_id': campaign_id,
            'supplier_id': supplier_id,
        }
        field.update(added_fields)
        items.append(LeadsFormItems(**field))
        current_entry_id = 1
        name = field['key_name']
        for lead in leads_old_object:
            col_value = getattr(lead, name)
            if col_value is not None:
                data.append(LeadsFormData(**{
                    'supplier_id': supplier_id,
                    'campaign_id': campaign_id,
                    'item_id': order_id,
                    'item_value': col_value,
                    'leads_form_id': current_form_id,
                    'entry_id': current_entry_id,
                    'created_at': lead.created_at,
                    'updated_at': lead.updated_at,
                    }))
            current_entry_id = current_entry_id + 1

    leads_form_details = LeadsForm(**{
             'campaign_id': campaign_id,
             'fields_count': len(items),
             'last_entry_id': current_entry_id-1
             })
    leads_form_details.save()
    for item in items:
        item.save()
    #LeadsFormItems.objects.bulk_create(items)
    LeadsFormData.objects.bulk_create(data)

class MigrateLeadsData(APIView):

    def put(self, request):
        class_name = self.__class__.__name__
        leads_old = Leads.objects.all()
        unique_forms = leads_old.values('object_id','campaign_id').distinct()

        fields = {
            'firstname1': 'STRING',
            'firstname2': 'STRING',
            'lastname1': 'STRING',
            'lastname2': 'STRING',
            'mobile1': 'INT',
            'mobile2': 'INT',
            'phone': 'INT',
            'email1': 'EMAIL',
            'email2': 'EMAIL',
            'address': 'TEXTAREA',
            'alphanumeric1': 'STRING',
            'alphanumeric2': 'STRING',
            'alphanumeric3': 'STRING',
            'alphanumeric4': 'STRING',
            'boolean1': 'INT',
            'boolean2': 'INT',
            'boolean3': 'INT',
            'boolean4': 'INT',
            'float1': 'FLOAT',
            'float2': 'FLOAT',
            'date1': 'DATE',
            'date2': 'DATE',
            'number1': 'INT',
            'number2': 'INT',
            'is_interested': 'INT'
        }

        fixed_fields = [
            {'key_name': 'is_from_sheet', 'key_type': 'BOOLEAN'}
        ]

        leads_query = LeadsForm.objects.order_by('-id')
        last_form_id = leads_query[0].id if len(leads_query) > 0 else 0
        last_entry_id = leads_query[0].last_entry_id if len(leads_query) > 0 else 0
        if last_entry_id is None:
            last_entry_id = 0
        form_id = last_form_id
        entry_id = last_entry_id+1
        # iterating by form
        for form in unique_forms:
            campaign_id = form["campaign_id"]
            supplier_id = form["object_id"]
            form_id = form_id+1
            save_items(fields, fixed_fields, form, form_id, entry_id)
        # leads form import successful
            leads_old_data = leads_old.filter(campaign_id=campaign_id, object_id=supplier_id)
            alias_data_object = LeadAlias.objects.filter(campaign_id=campaign_id)
            # iterating by enteries for a given form

        return ui_utils.handle_response({}, data='success', success=True)

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
         contacts_data_object = LeadsFormContacts.objects.filter(form_id=form_id).values('contact_name','contact_mobile')
         contacts_data = []
         for data in contacts_data_object:
            contacts_data.append(data)
         return ui_utils.handle_response(class_name, data=contacts_data, success=True)

