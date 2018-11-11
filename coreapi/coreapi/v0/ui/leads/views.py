from rest_framework.views import APIView
from openpyxl import load_workbook, Workbook
from models import (LeadsForm, LeadsFormItems, LeadsFormData, LeadsFormContacts, get_leads_summary)
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.inventory.models import (InventoryActivityAssignment, InventoryActivity)
import operator
import v0.ui.utils as ui_utils
import boto3
import os
import datetime
from bulk_update.helper import bulk_update
from v0.ui.common.models import BaseUser
from v0.ui.campaign.models import CampaignAssignment
from v0.constants import campaign_status, proposal_on_hold
from django.http import HttpResponse
from celery import shared_task
from django.conf import settings
from v0.ui.common.models import mongo_client, mongo_test
import pprint
from random import randint
import random
import string
pp = pprint.PrettyPrinter(depth=6)
import hashlib


def enter_lead_to_mongo(lead_data, supplier_id, campaign_id, lead_form, entry_id):
    all_form_items_dict = lead_form['data']
    timestamp = datetime.datetime.utcnow()
    lead_dict = {"data": [], "is_hot": False, "created_at": timestamp, "supplier_id": supplier_id, "campaign_id": campaign_id,
                 "leads_form_id": lead_form['leads_form_id'], "entry_id": entry_id, "status": "active"}
    for lead_item_data in lead_data:
        if "value" not in lead_item_data:
            continue
        item_dict = {}
        item_id = lead_item_data["item_id"]
        key_name = all_form_items_dict[str(item_id)]["key_name"]
        key_type = all_form_items_dict[str(item_id)]["key_type"]
        value = lead_item_data["value"]
        lead_dict["data"].append({
            'key_name': key_name,
            'value': value,
            'item_id': item_id,
            'key_type': key_type
        })

        if value:
            if "hot_lead_criteria" in all_form_items_dict[str(item_id)]:
                if all_form_items_dict[str(item_id)]["hot_lead_criteria"] and value == all_form_items_dict[str(item_id)]["hot_lead_criteria"]:
                    lead_dict["is_hot"] = True
            elif 'counseling' in key_name.lower():
                lead_dict["is_hot"] = True
    lead_sha_256 = create_lead_hash(lead_dict)
    lead_dict["lead_sha_256"] = lead_sha_256
    lead_already_exist = True if len(list(mongo_client.leads.find({"lead_sha_256": lead_sha_256}))) > 0 else False
    if not lead_already_exist:
        mongo_client.leads.insert_one(lead_dict).inserted_id
    return


def convertToNumber(str):
    try:
        return int(str)
    except ValueError:
        return str


def get_supplier_all_leads_entries(leads_form_id, supplier_id, page_number=0, **kwargs):
    leads_per_page = 25
    leads_forms = mongo_client.leads_forms.find_one({"leads_form_id": int(leads_form_id)}, {"_id":0, "data":1})
    leads_forms_items = leads_forms["data"]
    if supplier_id == 'All':
        leads_data = mongo_client.leads.find({"$and": [{"leads_form_id": int(leads_form_id)}, {"status": {"$ne": "inactive"}}]},
                                              {"_id": 0})
        leads_data_list = list(leads_data)
        suppliers_list = []
        for lead_data in leads_data_list:
            suppliers_list.append(lead_data['supplier_id'])
        suppliers_list = list(set(suppliers_list))
        suppliers_names = SupplierTypeSociety.objects.filter(supplier_id__in=suppliers_list).values_list(
            'supplier_id','society_name')
        supplier_id_names = dict((x, y) for x, y in suppliers_names)
    else:
        leads_data = mongo_client.leads.find({"$and": [{"leads_form_id": int(leads_form_id)}, {"supplier_id": supplier_id},
                                                       {"status": {"$ne": "inactive"}}]}, {"_id": 0})
        leads_data_list = list(leads_data)
        supplier_data = SupplierTypeSociety.objects.get(supplier_id=supplier_id)
        supplier_name = supplier_data.society_name

    hot_leads = [x['entry_id'] for x in leads_data_list if x['is_hot'] == True]
    headers = []
    for form_item in leads_forms_items:
        curr_item = leads_forms_items[form_item]
        headers.append({
            "order_id": curr_item["order_id"] if "order_id" in curr_item else None,
            "key_name": curr_item["key_name"],
            "hot_lead_criteria": curr_item["hot_lead_criteria"] if "hot_lead_criteria" in curr_item else None
        })
    headers.extend(({
        "order_id": 0,
        "key_name": "Supplier Name"
    },
        {
            "order_id": 0,
            "key_name": "Lead Date"
        }))
    headers = sorted(headers,key=operator.itemgetter('order_id'))

    values = []

    if 'start_date' in kwargs and kwargs['start_date']:
        leads_data_start = [x for x in leads_data_list if x['created_at'].date() >= kwargs['start_date']]
        leads_data_list = leads_data_start
    if 'end_date' in kwargs and kwargs['end_date']:
        leads_data_start_end = [x for x in leads_data_start if x['created_at'].date() <= kwargs['end_date']]
        leads_data_list = leads_data_start_end

    # first_entry = (page_number-1)*leads_per_page+1
    # if first_entry>len(leads_data_list):
    #     leads_data_list_paginated = []
    # else:
    #     last_entry = min(page_number*leads_per_page, len(leads_data_list))
    #     leads_data_list_sorted = list(set(leads_data_list))
    #     leads_data_list_paginated = leads_data_list_sorted[first_entry:(last_entry-1)]
    #leads_data_values_itemid = [x["data"] for x in leads_data_list]
    leads_data_values = []
    for entry in leads_data_list:
        curr_entry = entry['data']
        entry_date = entry['created_at']
        if supplier_id == 'All':
            curr_supplier_id = entry['supplier_id']
            curr_supplier_name = supplier_id_names[curr_supplier_id]
        else:
            curr_supplier_name = supplier_name
        new_entry = [
            {
                "order_id": 0,
                "value": curr_supplier_name
            },
            {
                "order_id": 0,
                "value": entry_date
            }
        ]
        for item in curr_entry:
            value = None
            if item["value"]:
                if isinstance(item["value"], basestring):
                    value = item["value"].encode('utf8').strip()
                value = convertToNumber(item["value"])  # if possible

            new_entry.append({"order_id": item["item_id"], "value": value})
        leads_data_values.append(new_entry)

    final_data = {"hot_leads": hot_leads, "headers": headers, "values": leads_data_values}

    return final_data


class GetLeadsEntries(APIView):
    @staticmethod
    def get(request, leads_form_id):
        supplier_id = str(request.query_params.get('supplier_id')) if request.query_params.get('supplier_id'
                                                                                              ) is not None else 'All'

        page_number = int(request.query_params.get('page_number',0))
        supplier_all_lead_entries = get_supplier_all_leads_entries(leads_form_id, supplier_id,page_number)
        return ui_utils.handle_response({}, data=supplier_all_lead_entries, success=True)

class GetLeadsEntriesBySupplier(APIView):
    @staticmethod
    def get(request, leads_form_id, supplier_id):
        page_number = int(request.query_params.get('page_number', 0))
        supplier_all_lead_entries = get_supplier_all_leads_entries(leads_form_id, supplier_id,page_number)
        return ui_utils.handle_response({}, data=supplier_all_lead_entries, success=True)


class GetLeadsEntriesByCampaignId(APIView):
    # it is assumed that a form belongs to a campaign
    @staticmethod
    def get(request, campaign_id, supplier_id='All'):
        page_number = int(request.query_params.get('page_number', 0))
        first_leads_form_id = mongo_client.leads_forms.find_one({"campaign_id":campaign_id})['leads_form_id']
        supplier_all_lead_entries = get_supplier_all_leads_entries(first_leads_form_id, supplier_id, page_number)
        return ui_utils.handle_response({}, data=supplier_all_lead_entries, success=True)


class CreateLeadsForm(APIView):
    @staticmethod
    def post(request, campaign_id):
        leads_form_name = request.data['leads_form_name']
        leads_form_items = request.data['leads_form_items']
        item_id = 0
        max_id_data = mongo_client.leads_forms.find_one(sort=[('leads_form_id', -1)])
        max_id = max_id_data['leads_form_id'] if max_id_data is not None else 0
        mongo_dict = {
            'leads_form_id': max_id+1,
            'campaign_id': campaign_id,
            'leads_form_name': leads_form_name,
            'data': {},
            'status': 'active'
        }
        for item in leads_form_items:
            item_id = item_id + 1
            key_options = item["key_options"] if 'key_options' in item else None
            if key_options and not isinstance(key_options, list):
                key_options = key_options.split(',')
            item["item_id"] = item_id
            mongo_dict['data'][str(item_id)] = item
        mongo_client.leads_forms.insert_one(mongo_dict)
        return ui_utils.handle_response({}, data='success', success=True)


class GetLeadsForm(APIView):
    @staticmethod
    def get(request, campaign_id):
        campaign_lead_form = mongo_client.leads_forms.find(
            {"$and": [{"campaign_id": campaign_id}, {"status": {"$ne": "inactive"}}]}, {"_id": 0})
        lead_form_dict = {}
        for lead_from in campaign_lead_form:
            lead_form_dict[lead_from["leads_form_id"]] = {
                "leads_form_name": lead_from['leads_form_name'],
                "leads_form_id": lead_from['leads_form_id'],
                "leads_form_items": lead_from['data']
            }
        return ui_utils.handle_response({}, data=lead_form_dict, success=True)


class LeadsFormBulkEntry(APIView):
    @staticmethod
    def post(request, leads_form_id):
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        lead_form = mongo_client.leads_forms.find_one({"leads_form_id": int(leads_form_id)})
        fields = len(lead_form['data'])
        campaign_id = lead_form['campaign_id']
        entry_id = lead_form['last_entry_id'] + 1 if 'last_entry_id' in lead_form else 1

        missing_societies = []
        inv_activity_assignment_missing_societies = []
        inv_activity_missing_societies = []
        not_present_in_shortlisted_societies = []
        more_than_ones_same_shortlisted_society = []
        unresolved_societies = []

        leads_dict = []
        all_sha256 = list(mongo_client.leads.find({"leads_form_id": int(leads_form_id)},{"lead_sha_256": 1, "_id": 0}))
        all_sha256_list = [str(element['lead_sha_256']) for element in all_sha256]
        for index, row in enumerate(ws.iter_rows()):

            if index == 0:
                for idx, i in enumerate(row):
                    if 'apartment' in i.value.lower():
                        apartment_index = idx
                        break
            if index > 0:
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

                created_at = inventory_activity_list[0].activity_date if inventory_activity_list[0].activity_date else None
                lead_dict = {"data": [], "is_hot": False, "created_at": created_at, "supplier_id": found_supplier_id,
                             "campaign_id": campaign_id, "leads_form_id": int(leads_form_id), "entry_id": entry_id}
                for item_id in range(0, fields):
                    curr_item_id = item_id + 1
                    curr_form_item_dict = lead_form['data'][str(curr_item_id)]
                    key_name = curr_form_item_dict['key_name']
                    hot_lead_criteria = None
                    if 'hot_lead_criteria' in curr_form_item_dict:
                        hot_lead_criteria = curr_form_item_dict['hot_lead_criteria'] if curr_form_item_dict[
                            'hot_lead_criteria'] else None
                    value = row[item_id].value if row[item_id].value else None
                    if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                        value = str(value)
                    if value:
                        if hot_lead_criteria is not None and value == hot_lead_criteria:
                            lead_dict["is_hot"] = True
                        elif 'counseling' in key_name.lower():
                            lead_dict["is_hot"] = True
                    item_dict = {
                        'key_name': key_name,
                        'value': value,
                        'item_id': curr_item_id
                    }
                    lead_dict["data"].append(item_dict)
                lead_sha_256 = create_lead_hash(lead_dict)
                lead_dict["lead_sha_256"] = lead_sha_256
                lead_already_exist = True if lead_sha_256 in all_sha256_list else False
                if not lead_already_exist:
                    mongo_client.leads.insert_one(lead_dict)
                    entry_id = entry_id + 1  # will be saved in the end
        missing_societies.sort()
        print "missing societies", missing_societies
        print "unresolved_societies", list(set(unresolved_societies))
        print "more_than_ones_same_shortlisted_society", list(set(more_than_ones_same_shortlisted_society))
        print "inv_activity_assignment_missing_societies", list(set(inv_activity_assignment_missing_societies))
        print "inv_activit_missing_societies", list(set(inv_activity_missing_societies))
        print "not_present_in_shortlisted_societies", list(set(not_present_in_shortlisted_societies))
        return ui_utils.handle_response({}, data='success', success=True)


class LeadsFormEntry(APIView):
    @staticmethod
    def post(request, leads_form_id):
        supplier_id = request.data['supplier_id']
        lead_form = mongo_client.leads_forms.find_one({"leads_form_id": int(leads_form_id)})
        entry_id = lead_form['last_entry_id'] + 1 if 'last_entry_id' in lead_form else 1
        campaign_id = lead_form['campaign_id']
        lead_data = request.data["leads_form_entries"]
        enter_lead_to_mongo(lead_data, supplier_id, campaign_id, lead_form, entry_id)
        return ui_utils.handle_response({}, data='success', success=True)


@shared_task()
def migrate_to_mongo():
    campaign_list = list(set(LeadsFormData.objects.values_list('campaign_id', flat=True)))
    for campaign_id in campaign_list:
        all_leads_data_object = LeadsFormData.objects.filter(campaign_id=campaign_id).all()
        all_leads_data = []
        for data in all_leads_data_object:
            all_leads_data.append(data.__dict__)
        all_leads_forms = LeadsForm.objects.all().values('id', 'campaign_id', 'leads_form_name', 'last_entry_id',
                                                         'status', "fields_count", "last_contact_id", "created_at")
        all_leads_items = LeadsFormItems.objects.all().values('leads_form_id', 'item_id', 'key_name', 'hot_lead_criteria',
                                                              'key_options', 'order_id', 'status', 'is_required',
                                                              'key_type',
                                                              'campaign_id', 'supplier_id')
        all_leads_items_dict = {}
        for lead_item in all_leads_items:
            if lead_item['leads_form_id'] not in all_leads_items_dict:
                all_leads_items_dict[lead_item['leads_form_id']] = []
            all_leads_items_dict[lead_item['leads_form_id']].append(lead_item)
        for leads_form in all_leads_forms:
            mongo_dict = {
                'leads_form_id': leads_form['id'],
                'campaign_id': leads_form['campaign_id'],
                'leads_form_name': leads_form['leads_form_name'],
                'last_entry_id': leads_form['last_entry_id'],
                'status': leads_form['status'],
                'last_contact_id': leads_form['last_contact_id'],
                'created_at': leads_form['created_at'],
                'data': {}
            }
            if leads_form['id'] in all_leads_items_dict:
                for item in all_leads_items_dict[leads_form['id']]:
                    key_options = item["key_options"] if 'key_options' in item else None
                    mongo_dict['data'][str(item['item_id'])] = {
                        'item_id': item['item_id'],
                        'key_type': item['key_type'],
                        'key_name': item['key_name'],
                        'key_options': key_options,
                        'order_id': item['order_id'],
                        'status': item['status'],
                        'leads_form_id': item['leads_form_id'],
                        'is_required': item['is_required'],
                        'hot_lead_criteria': item['hot_lead_criteria'],
                        'campaign_id': item['campaign_id'],
                        'supplier_id': item['supplier_id'],

                    }
            mongo_client.leads_forms.insert_one(mongo_dict)
        leads_form_ids = all_leads_data_object.values_list('leads_form_id', flat=True).distinct()
        for curr_form_id in leads_form_ids:
            curr_form_id = curr_form_id
            curr_form_data = [x for x in all_leads_data if x['leads_form_id'] == curr_form_id]
            curr_form_items = [x for x in all_leads_items if x['leads_form_id'] == curr_form_id]
            first_data_element = curr_form_data[0]
            campaign_id = first_data_element['campaign_id']
            entry_ids = list(set([x['entry_id'] for x in curr_form_data]))
            entry_count = 0
            for curr_entry_id in entry_ids:
                entry_count = entry_count + 1
                curr_entry_data = [x for x in curr_form_data if x['entry_id'] == curr_entry_id]
                supplier_id = curr_entry_data[0]['supplier_id']
                created_at = curr_entry_data[0]['created_at']
                lead_dict = {"data": [], "is_hot": False, "created_at": created_at, "supplier_id": supplier_id,
                             "campaign_id": campaign_id, "leads_form_id": curr_form_id, "entry_id": curr_entry_id,
                             "status": "active"}
                for curr_data in curr_entry_data:
                    item_id = curr_data['item_id']
                    value = curr_data['item_value']
                    curr_item = [x for x in curr_form_items if x['item_id'] == item_id][0]
                    key_name = curr_item['key_name']
                    key_type = curr_item['key_type']
                    item_dict = {
                        'item_id': item_id,
                        'key_name': key_name,
                        'value': value,
                        'key_type': key_type
                    }
                    lead_dict['data'].append(item_dict)
                    if value:
                        if curr_item['hot_lead_criteria'] and value == curr_item['hot_lead_criteria']:
                            lead_dict["is_hot"] = True
                        elif 'counseling' in key_name.lower():
                            lead_dict["is_hot"] = True
                mongo_client.leads.insert_one(lead_dict)
    return


class MigrateLeadsToMongo(APIView):
    def put(self, request):
        class_name = self.__class__.__name__
        migrate_to_mongo.delay()
        return ui_utils.handle_response(class_name, data='success', success=True)


@shared_task()
def sanitize_leads_data():
    campaign_list = list(set(LeadsFormData.objects.values_list('campaign_id', flat=True)))
    for campaign_id in campaign_list:
        all_leads_data = LeadsFormData.objects.filter(campaign_id=campaign_id).all().order_by("-entry_id")
        last_entry_id = all_leads_data[0].entry_id if len(all_leads_data) > 0 else None
        lead_form = LeadsForm.objects.get(campaign_id=campaign_id)
        LeadsFormData.objects.filter(campaign_id=campaign_id).all()
        new_entry_id = last_entry_id + 1 if last_entry_id else 1
        all_leads_items = LeadsFormItems.objects.filter(campaign_id=campaign_id).all()
        scholarship_item_id = None
        other_child_item_id = None
        counseling_item_id = None
        other_child_class_item_id = None
        first_child_name_item_id = None
        first_child_class_item_id = None
        for item in all_leads_items:
            if "scholarship" in item.key_name.lower():
                scholarship_item_id = item.item_id
            if "name of other child" in item.key_name.lower():
                other_child_item_id = item.item_id
            if "counseling" in item.key_name.lower() or "counselling" in item.key_name.lower() or "counceling" in item.key_name.lower():
                counseling_item_id = item.item_id
            if "class of other child" in item.key_name.lower() or "class of second child" in item.key_name.lower():
                other_child_class_item_id = item.item_id
            if "name of first child" in item.key_name.lower() or "name of child" in item.key_name.lower():
                first_child_name_item_id = item.item_id
            if "class of first child" in item.key_name.lower():
                first_child_class_item_id = item.item_id
        all_leads_data_dict = {}

        for lead_data in all_leads_data:
            if lead_data.entry_id not in all_leads_data_dict:
                all_leads_data_dict[lead_data.entry_id] = []
            all_leads_data_dict[lead_data.entry_id].append({
                "created_at": lead_data.created_at,
                "updated_at": lead_data.updated_at,
                "supplier_id": lead_data.supplier_id,
                "item_id": lead_data.item_id,
                "item_value": lead_data.item_value,
                "leads_form_id": lead_data.leads_form_id,
                "entry_id": lead_data.entry_id,
                "status": lead_data.status,
                "campaign_id": lead_data.campaign_id
            })
        for entry_id in all_leads_data_dict:
            entry_data = all_leads_data_dict[entry_id]
            convert_counseling = False
            create_other_child_lead = False
            other_child_name = None
            other_child_class = None
            for item in entry_data:
                if item['item_id'] == scholarship_item_id:
                    if item['item_value'] == "NA":
                        convert_counseling = True
                if item['item_id'] == other_child_item_id:
                    if item['item_value'] and len(item['item_value']) > 2:
                        create_other_child_lead = True
                        other_child_name = item['item_value']
                        item_object = LeadsFormData.objects.filter(entry_id=item['entry_id'], item_id=item['item_id'])
                        item_object.update(item_value=None)
                if item['item_id'] == other_child_class_item_id:
                    if create_other_child_lead:
                        item_object = LeadsFormData.objects.filter(entry_id=item['entry_id'], item_id=item['item_id'])
                        item_object.update(item_value=None)
                if item['item_id'] == other_child_class_item_id:
                    other_child_class = item['item_value']
            if convert_counseling:
                for item in entry_data:
                    if item['item_id'] == counseling_item_id:
                        if not item['item_value']:
                            item_object = LeadsFormData.objects.filter(entry_id=item['entry_id'],
                                                                       item_id=item['item_id'])
                            item_object.update(item_value="CounselingScheduled")
            if create_other_child_lead:
                item_list = []
                for item in entry_data:
                    item['entry_id'] = new_entry_id
                    if item['item_id'] == other_child_item_id:
                        item['item_value'] = None
                    if item['item_id'] == other_child_class_item_id:
                        item['item_value'] = None
                    if item['item_id'] == first_child_name_item_id:
                        item['item_value'] = other_child_name
                    if item['item_id'] == first_child_class_item_id:
                        item['item_value'] = other_child_class
                    item_list.append(LeadsFormData(**item))
                LeadsFormData.objects.bulk_create(item_list)
                new_entry_id += 1
        LeadsForm.objects.filter(campaign_id=campaign_id).update(last_entry_id=new_entry_id - 1)
        return


class SanitizeLeadsData(APIView):
    def put(self, request):
        class_name = self.__class__.__name__
        sanitize_leads_data.delay()
        return ui_utils.handle_response(class_name, data='success', success=True)


def write_keys_to_file(keys_list):
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
    return filename

class GenerateLeadForm(APIView):
    @staticmethod
    def get(request, leads_form_id):
        leads_form_data_mongo = mongo_client.leads_forms.find_one({"leads_form_id": int(leads_form_id)},{"data":1, "_id":0})
        leads_form_data = leads_form_data_mongo["data"]
        keys_list = ['supplier_id', 'lead_entry_date (format: dd/mm/yyyy)']
        for lead in leads_form_data:
            keys_list.append(leads_form_data[lead]["key_name"])
        filename = write_keys_to_file(keys_list)
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
            value_list.append(item_dict["value"])
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

class DeleteLeadForm(APIView):
    # Entire form is deactivated
    @staticmethod
    def put(request, form_id):
        result = mongo_client.leads_forms.update_one({"leads_form_id": int(form_id)},
                                     {"$set": {"status": "inactive"}})
        return ui_utils.handle_response({}, data='success', success=True)


class DeleteLeadEntry(APIView):
    @staticmethod
    def put(request, form_id, entry_id):
        result = mongo_client.leads.update_one({"leads_form_id": int(form_id), "entry_id": int(entry_id)},
                                     {"$set": {"status": "inactive"}})
        return ui_utils.handle_response(result, data='success', success=True)


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


class AddLeadFormItems(APIView):
    # this function is used to add
    def put(self, request, form_id):
        class_name = self.__class__.__name__
        items_dict_list = request.data
        for items_dict in items_dict_list:
            old_form = mongo_client.leads_forms.find_one({"leads_form_id": int(form_id)})
            if not old_form:
                return ui_utils.handle_response(class_name, data={"status": "No for Found with this id"}, success=True)
            old_form_items = old_form['data']
            max_item_id = 0
            max_order_id = 0
            for item in old_form_items:
                if int(item) > max_item_id:
                    max_item_id = int(item)
                if 'order_id' in old_form_items[item] and old_form_items[item]['order_id'] > max_order_id:
                   max_order_id = int(old_form_items[item]['order_id'])
            new_form_item = {
                "key_name": items_dict['key_name'],
                "campaign_id": old_form['campaign_id'],
                "hot_lead_criteria": items_dict["hot_lead_criteria"] if "hot_lead_criteria"  in items_dict else None,
                "key_type": items_dict["key_type"],
                "key_options": items_dict["key_options"] if "key_options" in items_dict else None,
                "leads_form_id": form_id,
                "is_required": items_dict["is_required"] if "is_required" in items_dict else None,
                "item_id": max_item_id + 1,
                "order_id": max_order_id + 1,
            }
            old_form_items[str(max_item_id + 1)] = new_form_item
            mongo_client.leads_forms.update_one({"leads_form_id": int(form_id)}, {"$set": {"data": old_form_items}})
        return ui_utils.handle_response(class_name, data='success', success=True)


class EditLeadsForm(APIView):
    @staticmethod
    def put(request, form_id):
        name = request.data['name'] if 'name' in request.data.keys() else None
        if name is not None:
            mongo_client.leads_forms.update_one({"leads_form_id": int(form_id)}, {"$set": {"leads_form_name": name}})
        return ui_utils.handle_response({}, data='success', success=True)


class GenerateDemoData(APIView):
    def put(self, request):
        #leads_form_test_data = mongo_test.leads_forms.find_one({"leads_form_id": 13})
        leads_data_all = mongo_client.leads.find({})
        # copy leads form data
        leads_form_object = mongo_client.leads_forms.find({})
        leads_form_all = list(leads_form_object)
        for curr_form in leads_form_all:
            mongo_test.leads_forms.insert_one(curr_form)
        for curr_lead in leads_data_all:
            leads_form_id = curr_lead['leads_form_id']
            curr_leads_form = [x for x in leads_form_all if x['leads_form_id'] == leads_form_id]
            curr_data = curr_lead['data']
            new_data = []
            for curr_data_item in curr_data:
                item_id = curr_data_item['item_id']
                curr_leads_form_items = curr_leads_form[0]['data']
                curr_leads_form_item = curr_leads_form_items[str(item_id)]
                key_name = curr_data_item['key_name']
                key_type = curr_leads_form_item['key_type']
                if 'number' in key_name.lower() or 'phone' in key_name.lower():
                    curr_data_item['value'] = randint(9000000000,9999999999)
                allchar = string.ascii_letters.lower()
                if 'email' in key_type.lower():
                    r1 = "".join(random.choice(allchar) for x in range(randint(4, 6)))
                    r2 = "".join(random.choice(allchar) for x in range(randint(4, 6)))
                    curr_data_item['value'] = r1+'@'+r2 + '.com'
                if 'name' in key_name.lower():
                    if 'apartment' not in key_name.lower():
                        curr_data_item['value'] = "".join(random.choice(allchar) for x in range(randint(6, 10)))
                curr_data_item['key_type'] = key_type
                new_data.append(curr_data_item)
            curr_lead['data'] = new_data
            mongo_test.leads.insert_one(curr_lead)


            #name_data = [x for x in curr_lead if 'name' in x['key_name'].to_lower()]


        # for form in leads_form_all:
        #     curr_form_id = form['leads_form_id']
        #     print curr_form_id
        #     curr_form_data = form['data']
        #     form_keys = curr_form_data.keys()
        #     form_values = curr_form_data.values()
        #     # for item_id in form_keys:
        #     #     curr_item_data = curr_form_data[item_id]
        #     #     email_fields = [x for x in curr_item_data]
        #     email_form = False
        #     phone_form = False
        #     email_fields = [x for x in form_values if x['key_type'].tolower() == 'email']
        #     phone_fields = [x for x in form_values if x['key_type'].tolower() == 'phone']


        return ui_utils.handle_response({}, data='success', success=True)


class LeadsSummary(APIView):

    def get(self, request):
        class_name = self.__class__.__name__
        username = request.user
        user_id = BaseUser.objects.get(username=username).id
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=user_id).values_list('campaign_id', flat=True).distinct()
        campaign_list = [campaign_id for campaign_id in campaign_list]
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
        all_campaign_summary = get_leads_summary(campaign_list)
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


def create_lead_hash(lead_dict):
    lead_hash_string = ''
    lead_hash_string += str(lead_dict['leads_form_id'])

    for item in lead_dict['data']:
        if item['value']:
            if isinstance(item["value"], basestring):
                lead_hash_string += str(item['value'].encode('utf-8').strip())
            else:
                lead_hash_string += str(item['value'])
    return hashlib.sha256(lead_hash_string).hexdigest()


class UpdateLeadsDataSHA256(APIView):
    def put(self, request):
        refresh_all = request.data['refresh_all'] if 'refresh_all' in request.data else False
        find_param = {"lead_sha_256": {"$exists": False}}
        if refresh_all:
            find_param = {}
        leads_data_all = mongo_client.leads.find(find_param, no_cursor_timeout=True)
        bulk = mongo_client.leads.initialize_unordered_bulk_op()
        counter = 0
        for curr_lead in leads_data_all:
            entry_id = curr_lead['entry_id']
            lead_sha_256 = create_lead_hash(curr_lead)
            bulk.find({"entry_id": int(entry_id)}).update({"$set": {"lead_sha_256": lead_sha_256}})
            counter += 1
            if counter % 500 == 0:
                bulk.execute()
                bulk = mongo_client.leads.initialize_unordered_bulk_op()
        if counter > 0:
            bulk.execute()
        return ui_utils.handle_response({}, data='success', success=True)


def create_global_hot_lead_criteria(curr_lead_form):
    global_hot_lead_criteria = {
        'or':{},
    }
    items_dict = curr_lead_form['data']
    for item in items_dict:
        key_name = items_dict[item]['key_name'].lower()
        if 'hot_lead_criteria' in items_dict[item] and items_dict[item]['hot_lead_criteria']:
            global_hot_lead_criteria['or'][item] = [items_dict[item]['hot_lead_criteria']]
            if items_dict[item]['hot_lead_criteria'] == 'Y':
                global_hot_lead_criteria['or'][item] += ['y','Yes', 'yes', 'YES']
        if "counseling" in key_name or "counselling" in key_name or "counceling" in key_name:
            global_hot_lead_criteria['or'][item] = ['AnyValue']
    return global_hot_lead_criteria


class UpdateGlobalHotLeadCriteria(APIView):
    def put(self, request):
        refresh_all = request.data['refresh_all'] if 'refresh_all' in request.data else False
        find_param = {"global_hot_lead_criteria": {"$exists": False}}
        if refresh_all:
            find_param = {}
        leads_form_all = mongo_client.leads_forms.find(find_param, no_cursor_timeout=True)
        bulk = mongo_client.leads_forms.initialize_unordered_bulk_op()
        counter = 0
        for curr_lead_form in leads_form_all:
            leads_form_id = curr_lead_form['leads_form_id']
            global_hot_lead_criteria = create_global_hot_lead_criteria(curr_lead_form)
            bulk.find({"leads_form_id": int(leads_form_id)}).update({"$set": {"global_hot_lead_criteria": global_hot_lead_criteria}})
            counter += 1
            if counter % 500 == 0:
                bulk.execute()
                bulk = mongo_client.leads.initialize_unordered_bulk_op()
        if counter > 0:
            bulk.execute()
        return ui_utils.handle_response({}, data='success', success=True)

def calculate_is_hot(curr_lead, global_hot_lead_criteria):
    # checking 'or' global_hot_lead_criteria
    curr_lead_data_dict = {str(item['item_id']):item for item in curr_lead['data']}
    for item_id in global_hot_lead_criteria['or']:
        if item_id in curr_lead_data_dict and curr_lead_data_dict[item_id]['value'] is not None:
            print "here", curr_lead['leads_form_id'], curr_lead['entry_id'], item_id, str(curr_lead_data_dict[item_id]['value']).lower(), global_hot_lead_criteria['or'][item_id]
            if str(curr_lead_data_dict[item_id]['value']).lower() in global_hot_lead_criteria['or'][item_id]:
                print "in correct criteria"
                return True
            if "AnyValue" in global_hot_lead_criteria['or'][item_id]:
                print " in any value "
                return True
    return False

class UpdateLeadsDataIsHot(APIView):
    def put(self, request):
        leads_form_all = mongo_client.leads_forms.find({}, no_cursor_timeout=True)
        for leads_form_curr in leads_form_all:
            leads_form_id = leads_form_curr['leads_form_id']
            global_hot_lead_criteria = leads_form_curr['global_hot_lead_criteria']
            leads_data_all = mongo_client.leads.find({"leads_form_id": leads_form_id}, no_cursor_timeout=True)
            bulk = mongo_client.leads.initialize_unordered_bulk_op()
            counter = 0
            for curr_lead in leads_data_all:
                entry_id = curr_lead['entry_id']
                is_hot = calculate_is_hot(curr_lead, global_hot_lead_criteria)
                bulk.find({"entry_id": int(entry_id)}).update({"$set": {"is_hot": is_hot}})
                counter += 1
                if counter % 500 == 0:
                    bulk.execute()
                    bulk = mongo_client.leads.initialize_unordered_bulk_op()
            if counter > 0:
                bulk.execute()
        return ui_utils.handle_response({}, data='success', success=True)
