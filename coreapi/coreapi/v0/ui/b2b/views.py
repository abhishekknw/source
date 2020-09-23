from __future__ import print_function
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import (Requirement, SuspenseLead, BrowsedLead)
from .serializers import RequirementSerializer
import v0.ui.utils as ui_utils
from openpyxl import load_workbook
from v0.ui.account.models import ContactDetails, BusinessTypes
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, ProposalCenterMapping
from v0.ui.organisation.models import Organisation
from v0.ui.organisation.serializers import OrganisationSerializer
from django.db.models import Q
import v0.ui.utils as ui_utils
import datetime
from v0.ui.common.models import mongo_client
import hashlib
from v0.ui.common.pagination import paginateMongo
import json

def get_value_from_list_by_key(list1, key):
    text = ""
    try:
        text = list1[key].value
        text = text.strip()
    except:
        pass
    return text

class ImportLead(APIView):

    def post(self, request, campaign_id):
        data = request.data.copy()
        source_file = data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        headers = {}

        center = ProposalCenterMapping.objects.filter(proposal_id=campaign_id).first()
        for index, row in enumerate(ws.iter_rows()):
            if index == 0:
                i = 0
                for key in row:
                    key1 = key.value.lower()
                    key1 = key1.strip()
                    headers[key1] = i
                    i+=1
            else:
                # Parsing excel columns
                phone_number = get_value_from_list_by_key(row, headers.get('phone number'))
                supplier_name = get_value_from_list_by_key(row, headers.get('supplier name'))
                city = get_value_from_list_by_key(row, headers.get('city'))
                area = get_value_from_list_by_key(row, headers.get('area'))
                sector_name = get_value_from_list_by_key(row, headers.get('sector'))
                impl_timeline = get_value_from_list_by_key(row, headers.get('implementation timeline'))
                meating_timeline = get_value_from_list_by_key(row, headers.get('meating timeline'))
                lead_status = get_value_from_list_by_key(row, headers.get('lead status'))
                comment = get_value_from_list_by_key(row, headers.get('comment'))
                current_patner = get_value_from_list_by_key(row, headers.get('current partner'))
                prefered_patners = get_value_from_list_by_key(row, headers.get('prefered partners'))
                submitted = get_value_from_list_by_key(row, headers.get('submitted'))
                
                prefered_patners_array = []
                if prefered_patners:
                    prefered_patners_split = prefered_patners.split(",")
                    prefered_patners_array = [row.strip() for row in prefered_patners_split]

                contact_details = None
                if phone_number:
                    contact_details = ContactDetails.objects.filter(Q(mobile=phone_number)|Q(landline=phone_number)).first()
                
                supplier_id = ""
                supplier_type = "RS"

                supplier_conditions = {}
                supplier = None
                if contact_details:
                    supplier_id = contact_details.object_id
                    supplier = SupplierTypeSociety.objects.filter(supplier_id=supplier_id).first()

                    if not supplier:
                        supplier = SupplierMaster.objects.filter(supplier_id=supplier_id).first()
                        supplier_type = supplier.supplier_type
                elif supplier_name and city and area:
                    supplier = SupplierTypeSociety.objects.filter(society_name=supplier_name, society_city=city, society_locality=area).first()
                    if not supplier:
                        supplier = SupplierMaster.objects.filter(supplier_name=supplier_name, city=city, area=area).first()
                        if supplier:
                            supplier_type = supplier.supplier_type

                if supplier:
                    supplier_id = supplier.supplier_id
                    city = ""
                    area = ""
                    

                    if supplier_type != "RS":
                        city = supplier.address_supplier.city
                        area = supplier.address_supplier.area
                    else:
                        city = supplier.society_city
                        area = supplier.society_locality
                    
                    shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id, object_id=supplier_id).first()
                    if not shortlisted_spaces:

                        content_type = ui_utils.get_content_type(supplier_type)

                        shortlisted_spaces = ShortlistedSpaces(
                            proposal_id=campaign_id,
                            center=center,
                            supplier_code=supplier_type,
                            object_id=supplier_id,
                            content_type=content_type.data['data'],
                            status='F',
                            user=request.user,
                            requirement_given='yes',
                            requirement_given_date=datetime.datetime.now()
                        )
                        shortlisted_spaces.save()
                    
                    sector = BusinessTypes.objects.filter(business_type=sector_name.lower()).first()

                    current_patner_obj = None
                    if current_patner:
                        current_patner_obj = Organisation.objects.filter(name=current_patner).first()

                    prefered_patners_list = []
                    prefered_patners_id_list = []
                    if prefered_patners_array:
                        prefered_patners_list = Organisation.objects.filter(name__in=prefered_patners_array).all()
                        prefered_patners_id_list = [row.organisation_id for row in prefered_patners_list]
                    
                    if not submitted and submitted.lower() == "yes":
                        shortlisted_spaces.color_code = 1
                        shortlisted_spaces.save()

                        companies = Organisation.objects.filter(business_type=sector)
                        for company in companies:
                            requirement = Requirement(
                                campaign_id=campaign_id,
                                shortlisted_spaces=shortlisted_spaces,
                                company = company,
                                current_company = current_patner_obj,
                                # preferred_company = prefered_patners_list,
                                sector = sector,
                                # sub_sector = models.ForeignKey('BusinessSubTypes', null=True, blank=True, on_delete=models.CASCADE)
                                lead_by = contact_details,
                                impl_timeline = impl_timeline.lower(),
                                meating_timeline = meating_timeline.lower(),
                                lead_status = lead_status,
                                comment = comment,
                                varified_ops = 'no',
                                varified_bd = 'no',
                                lead_date = datetime.datetime.now()
                            )
                            requirement.save()

                            if prefered_patners_list:
                                requirement.preferred_company.set(prefered_patners_list)
                    else:
                        if shortlisted_spaces.color_code != 1:
                            shortlisted_spaces.color_code = 2
                            shortlisted_spaces.save()

                        BrowsedLead(
                            supplier_id=supplier_id,
                            shortlisted_spaces_id=shortlisted_spaces.id,
                            campaign_id=campaign_id,
                            phone_number = phone_number,
                            supplier_name = supplier_name,
                            city = city,
                            area = area,
                            sector_id = sector.id if sector else None,
                            implementation_timeline = impl_timeline,
                            meating_timeline = meating_timeline,
                            lead_status = lead_status,
                            comment = comment,
                            current_patner_id = current_patner_obj.organisation_id if current_patner_obj else None,
                            prefered_patners = prefered_patners_id_list,
                            status="open",
                            created_at = datetime.datetime.now(),
                            updated_at = datetime.datetime.now()
                        ).save()

                else:
                    if not shortlisted_spaces.color_code in [1,2,3]:
                        shortlisted_spaces.color_code = 4
                        shortlisted_spaces.save()

                    SuspenseLead(
                        phone_number = phone_number,
                        supplier_name = supplier_name,
                        city = city,
                        area = area,
                        sector_name = sector_name,
                        implementation_timeline = impl_timeline,
                        meating_timeline = meating_timeline,
                        lead_status = lead_status,
                        comment = comment,
                        current_patner = current_patner,
                        prefered_patners = prefered_patners_array,
                        created_at = datetime.datetime.now(),
                        updated_at = datetime.datetime.now()
                    ).save()
        
        return ui_utils.handle_response({}, data={}, success=True)
    
class RequirementClass(APIView):
    
    def get(self, request):
        shortlisted_spaces_id = request.query_params.get("shortlisted_spaces_id")
        requirements = Requirement.objects.filter(shortlisted_spaces_id=shortlisted_spaces_id, is_deleted='no')
        sectors = [row.sector for row in requirements]

        requirement_data = RequirementSerializer(requirements, many=True).data

        companies = Organisation.objects.filter(business_type__in=sectors)
        companies_data = OrganisationSerializer(companies, many=True).data
        
        return ui_utils.handle_response({}, data={"requirements": requirement_data, "companies": companies_data}, success=True)

    def put(self, request):
        requirements = request.data.get("requirements")

        for requirement in requirements:
            requirement_objs = Requirement.objects.filter(id=requirement["id"]).first()
            requirement_data = RequirementSerializer(requirement_objs, data=requirement)

            if requirement_data.is_valid():
                requirement_data.save()
            else:
                return ui_utils.handle_response({}, data={"errors":requirement_data.errors}, success=False)
        
        return ui_utils.handle_response({}, data={}, success=True)
    
    def post(self, request):
        requirement_ids = request.data.get("requirement_ids")

        requirements = Requirement.objects.filter(id__in=requirement_ids)

        shortlisted_spaces = None

        for requirement in requirements:
            if requirement.varified_bd == "no":

                campaign = ProposalInfo.objects.filter(type_of_end_customer__formatted_name="b_to_b_l_d", account__organisation=requirement.company).first()
                if campaign:
                    center = ProposalCenterMapping.objects.filter(proposal=campaign).first()

                    shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal=campaign, object_id=requirement.shortlisted_spaces.object_id).first()
                    if not shortlisted_spaces:

                        content_type = ui_utils.get_content_type(requirement.shortlisted_spaces.supplier_code)

                        shortlisted_spaces = ShortlistedSpaces(
                            proposal=campaign,
                            center=center,
                            supplier_code=requirement.shortlisted_spaces.supplier_code,
                            object_id=requirement.shortlisted_spaces.object_id,
                            content_type=content_type.data['data'],
                            status='F',
                            user=request.user,
                            requirement_given='yes',
                            requirement_given_date=datetime.datetime.now()
                        )
                        shortlisted_spaces.save()
                    
                    lead_form = mongo_client.leads_forms.find_one({"campaign_id": campaign.proposal_id})
                    if lead_form:
                        self.insert_lead_data(lead_form, requirement, campaign)

                        requirement.varified_bd = "yes"
                        requirement.varified_bd_date = datetime.datetime.now()
                        requirement.save()
                    else:
                        return ui_utils.handle_response({}, data={"error":"No lead form of "+requirement.company.name}, success=True)
                else:
                    return ui_utils.handle_response({}, data={"error":"No campaign to lead distributor of "+requirement.company.name}, success=True)
        if shortlisted_spaces:
            requirement_exist = Requirement.objects.filter(shortlisted_spaces=shortlisted_spaces, varified_bd = "no").first()
            if not requirement_exist:
                browsed_leads = BrowsedLead.objects.raw({"shortlisted_spaces_id":shortlisted_spaces.id, "status":"closed"})
                
                if not browsed_leads:
                    shortlisted_spaces.color_code = 3

            
        return ui_utils.handle_response({}, data={}, success=True)

    def insert_lead_data(self, lead_form, requirement, campaign):
        entry_id = lead_form['last_entry_id'] + 1 if 'last_entry_id' in lead_form else 1
        lead_data = []
        
        supplier_name = ""
        supplier_city = ""
        supplier_area = ""
        supplier_subarea = ""
        supplier_primary_count = ""
        
        if requirement.shortlisted_spaces.supplier_code == 'RS':
            supplier = SupplierTypeSociety.objects.filter(supplier_id = requirement.shortlisted_spaces.object_id).first()

            if supplier:
                supplier_name = supplier.society_name
                supplier_city = supplier.society_city
                supplier_area = supplier.society_locality
                supplier_subarea = supplier.society_subarea
                supplier_primary_count = supplier.flat_count
        else:
            supplier = SupplierMaster.objects.filter(supplier_id = requirement.shortlisted_spaces.object_id).first()
            if supplier:
                supplier_name = supplier.supplier_name
                supplier_city = supplier.city
                supplier_area = supplier.area
                supplier_subarea = supplier.subarea
                supplier_primary_count = supplier.unit_primary_count
        
        prefered_patner = "No"
        
        for row in requirement.preferred_company.all():
            if requirement.company == row:
                prefered_patner = "Yes"
        
        current_patner = "No"
        if requirement.company == requirement.current_company:
            current_patner = "Yes"
        
        lead_status = requirement.lead_status
        lead_form_key = None
        for key, lead_form_keys in lead_form["data"].items():
            if lead_form_keys["key_name"] == lead_status:
                lead_form_key = lead_form_keys["item_id"]
        
        lead_form_key_2 = None
        if lead_form_key:
            for key, value in lead_form["global_hot_lead_criteria"].items():
                if value.get("or"):
                    for key1, value1 in value["or"].items():
                        
                        if str(key1) == str(lead_form_key):
                            lead_form_key_2 = key
            if lead_form_key_2 and lead_form["hotness_mapping"].get(lead_form_key_2):
                lead_status = lead_form["hotness_mapping"].get(lead_form_key_2)

        lead_data_dict = {
            "Supplier Name": supplier_name,
            "Supplier City": supplier_city,
            "Supplier Area": supplier_area,
            "Supplier Sub Area": supplier_subarea,
            "Primary Count": supplier_primary_count,
            "Prefered Patner": prefered_patner,
            "Current Patner": current_patner,
            "Lead Status": lead_status
        }

        lead_data = []
        i = 1
        for key, value in lead_data_dict.items():
            row = {
                    'key_name': key,
                    'value': value,
                    'item_id': i,
                    'key_type': 'STRING'
                }
            lead_data.append(row)

            i+=1

        lead_dict = {"data": lead_data, "is_hot": False, "created_at": datetime.datetime.now(), "supplier_id": requirement.shortlisted_spaces.object_id, "campaign_id": campaign.proposal_id,
                    "leads_form_id": lead_form['leads_form_id'], "entry_id": entry_id, "status": "active", "lead_status": requirement.lead_status}
        lead_for_hash = {
            "data": lead_data,
            "leads_form_id": lead_form['leads_form_id']
        }
        
        lead_sha_256 = self.create_lead_hash(lead_for_hash)
        lead_dict["lead_sha_256"] = lead_sha_256

        mongo_client.leads.insert_one(lead_dict)

        return True

    def create_lead_hash(self, lead_dict):
        lead_hash_string = ''
        lead_hash_string += str(lead_dict['leads_form_id'])

        for item in lead_dict['data']:
            if item['value']:
                if isinstance(item["value"], (str,bytes)):
                    lead_hash_string += str(item['value'].strip())
                else:
                    lead_hash_string += str(item['value'])
        return hashlib.sha256(lead_hash_string.encode('utf-8')).hexdigest()


def remove_suspense_lead_cron():

    # Remove suspense leads
    all_suspense_lead = SuspenseLead.objects.all()
    
    for row in all_suspense_lead:
        contact_details = ContactDetails.objects.filter(Q(mobile=row.phone_number)|Q(landline=row.phone_number)).first()
        
        if contact_details:
            row.delete()
    
    # Close browsed leads
    prev_24h = datetime.datetime.now() - datetime.timedelta(days=1)

    BrowsedLead.objects.raw({'status': 'open', 'created_at': {"$lte": prev_24h}}).update({"$set":{"status":"closed"}})

    return HttpResponse(status=201)


class SuspenseLeadClass(APIView):

    def get(self, request):
        all_suspense_lead = SuspenseLead.objects.values()
        
        data = paginateMongo(all_suspense_lead, request)
        
        list1 = []
        for row in data["list"]:
            row1 = dict(row)
            row1["_id"] = str(row1["_id"])
            list1.append(row1)

        data["list"] = list1
        return ui_utils.handle_response({}, data=data, success=True)

class BrowsedLeadClass(APIView):

    def get(self, request):
        shortlisted_spaces_id = request.query_params.get("shortlisted_spaces_id")
        browsed_leads = BrowsedLead.objects.raw({"shortlisted_spaces_id":shortlisted_spaces_id, "status":"closed"}).values()
        
        list1 = []
        for row in browsed_leads:
            row1 = dict(row)
            row1["_id"] = str(row1["_id"])
            list1.append(row1)

        return ui_utils.handle_response({}, data=list1, success=True)

class LeadOpsVerification(APIView):

    def post(self, request):
        requirement_ids = request.data.get("requirement_ids")

        requirements = Requirement.objects.filter(id__in=requirement_ids)

        for requirement in requirements:
            if requirement.varified_ops == "no":
                requirement.varified_ops = "yes"
                requirement.varified_ops_date = datetime.datetime.now()
                requirement.save()

        return ui_utils.handle_response({}, data={}, success=True)

class BrowsedToRequirement(APIView):

    def post(self, request):
        browsed_ids = request.data.get("browsed_ids")

        shortlisted_spaces = None

        for browsed_id in browsed_ids:
            browsed = dict(BrowsedLead.objects.raw({"_id": browsed_id}).values())
            print(browsed)
            # companies = Organisation.objects.filter(business_type=browsed.sector_id)
            # for company in companies:
            #     requirement = Requirement(
            #         campaign_id=campaign_id,
            #         shortlisted_spaces=shortlisted_spaces,
            #         company = company,
            #         current_company = current_patner_obj,
            #         # preferred_company = prefered_patners_list,
            #         sector = sector,
            #         # sub_sector = models.ForeignKey('BusinessSubTypes', null=True, blank=True, on_delete=models.CASCADE)
            #         lead_by = contact_details,
            #         impl_timeline = impl_timeline.lower(),
            #         meating_timeline = meating_timeline.lower(),
            #         lead_status = lead_status,
            #         comment = comment,
            #         varified_ops = 'no',
            #         varified_bd = 'no',
            #         lead_date = datetime.datetime.now()
            #     )
            #     requirement.save()

            #     if prefered_patners_list:
            #         requirement.preferred_company.set(prefered_patners_list)

        return ui_utils.handle_response({}, data={}, success=True)