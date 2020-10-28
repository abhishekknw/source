from __future__ import print_function
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import (Requirement, SuspenseLead, BrowsedLead)
from .serializers import RequirementSerializer
import v0.ui.utils as ui_utils
from openpyxl import load_workbook
from v0.ui.account.models import ContactDetails, BusinessTypes, BusinessSubTypes
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
from bson.objectid import ObjectId
from v0.ui.common.serializers import BaseUserSerializer

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
                sub_sector_name = get_value_from_list_by_key(row, headers.get('sub sector'))
                impl_timeline = get_value_from_list_by_key(row, headers.get('implementation timeline'))
                meating_timeline = get_value_from_list_by_key(row, headers.get('meating timeline'))
                lead_status = get_value_from_list_by_key(row, headers.get('lead status'))
                comment = get_value_from_list_by_key(row, headers.get('comment'))
                current_patner = get_value_from_list_by_key(row, headers.get('current partner'))
                current_patner_feedback = get_value_from_list_by_key(row, headers.get('current patner feedback'))
                current_patner_feedback_reason = get_value_from_list_by_key(row, headers.get('current patner feedback reason'))
                prefered_patners = get_value_from_list_by_key(row, headers.get('prefered partners'))
                submitted = get_value_from_list_by_key(row, headers.get('submitted'))
                l1_answers = get_value_from_list_by_key(row, headers.get('l1 answers'))
                l2_answers = get_value_from_list_by_key(row, headers.get('l2 answers'))
                
                prefered_patners_array = []
                if prefered_patners:
                    prefered_patners_split = prefered_patners.split(",")
                    prefered_patners_array = [row.strip() for row in prefered_patners_split]

                contact_details = None
                if phone_number:
                    contact_details = ContactDetails.objects.filter(Q(mobile=phone_number)|Q(landline=phone_number)).first()
                
                supplier_id = ""
                supplier_type = "RS"

                sector = BusinessTypes.objects.filter(business_type=sector_name.lower()).first()
                sub_sector = BusinessSubTypes.objects.filter(business_sub_type=sub_sector_name.lower()).first()

                supplier_conditions = {}
                supplier = None
                if contact_details:
                    requirement = Requirement.objects.filter(campaign_id = campaign_id, lead_by = contact_details, sub_sector = sub_sector, is_deleted='no').first()
                    if requirement:
                        continue

                    supplier_id = contact_details.object_id
                    supplier = SupplierTypeSociety.objects.filter(supplier_id=supplier_id).first()

                    if not supplier:
                        supplier = SupplierMaster.objects.filter(supplier_id=supplier_id).first()
                        if supplier:
                            supplier_type = supplier.supplier_type
                elif supplier_name and city and area:
                    supplier = SupplierTypeSociety.objects.filter(society_name=supplier_name, society_city=city, society_locality=area).first()
                    if not supplier:
                        supplier = SupplierMaster.objects.filter(supplier_name=supplier_name, city=city, area=area).first()
                        if supplier:
                            supplier_type = supplier.supplier_type
                
                # campaign = ProposalInfo.objects.filter(Q(type_of_end_customer="b_2_b_r_g")&Q(Q(name=supplier.stage)|Q(name=@supplier.city))).first()
                # campaign_id = campaign.proposal_id

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
                    
                    shortlisted_spaces.requirement_given = 'yes'
                    shortlisted_spaces.requirement_given_date=datetime.datetime.now()
                    shortlisted_spaces.save()

                    current_patner_obj = None
                    current_company_other = None
                    if current_patner:
                        current_patner_obj = Organisation.objects.filter(name=current_patner).first()
                        if not current_patner_obj:
                            current_company_other = current_patner

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
                    
                    if submitted and submitted.lower() == "yes":
                        shortlisted_spaces.color_code = 1
                        shortlisted_spaces.save()

                        companies = Organisation.objects.filter(business_type=sector)
                        for company in companies:
                            requirement = Requirement(
                                campaign_id=campaign_id,
                                shortlisted_spaces=shortlisted_spaces,
                                company = company,
                                current_company = current_patner_obj,
                                current_company_other = current_company_other,
                                is_current_patner = "yes" if current_patner_obj == company else "no",
                                current_patner_feedback = current_patner_feedback,
                                current_patner_feedback_reason = current_patner_feedback_reason,
                                preferred_company_other = preferred_company_other,
                                sector = sector,
                                sub_sector = sub_sector,
                                lead_by = contact_details,
                                impl_timeline = impl_timeline.lower(),
                                meating_timeline = meating_timeline.lower(),
                                lead_status = lead_status,
                                comment = comment,
                                varified_ops = 'no',
                                varified_bd = 'no',
                                lead_date = datetime.datetime.now(),
                                l1_answers = l1_answers,
                                l2_answers = l2_answers
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
                            sub_sector_id = sub_sector.id if sub_sector else None,
                            implementation_timeline = impl_timeline.lower(),
                            meating_timeline = meating_timeline.lower(),
                            lead_status = lead_status,
                            comment = comment,
                            current_patner_id = current_patner_obj.organisation_id if current_patner_obj else None,
                            current_patner_other = current_company_other,
                            current_patner_feedback = current_patner_feedback,
                            current_patner_feedback_reason = current_patner_feedback_reason,
                            prefered_patners = prefered_patners_id_list,
                            prefered_patner_other = preferred_company_other,
                            status="open",
                            created_at = datetime.datetime.now(),
                            updated_at = datetime.datetime.now(),
                            l1_answers = l1_answers,
                            l2_answers = l2_answers
                        ).save()

                else:

                    SuspenseLead(
                        phone_number = phone_number,
                        supplier_name = supplier_name,
                        city = city,
                        area = area,
                        sector_name = sector_name,
                        sub_sector_name = sub_sector_name,
                        implementation_timeline = impl_timeline.lower(),
                        meating_timeline = meating_timeline.lower(),
                        lead_status = lead_status,
                        comment = comment,
                        current_patner = current_patner,
                        current_patner_feedback = current_patner_feedback,
                        current_patner_feedback_reason = current_patner_feedback_reason,
                        prefered_patners = prefered_patners_array,
                        created_at = datetime.datetime.now(),
                        updated_at = datetime.datetime.now(),
                        l1_answers = l1_answers,
                        l2_answers = l2_answers
                    ).save()
        
        return ui_utils.handle_response({}, data={}, success=True)
    
class RequirementClass(APIView):
    
    def get(self, request):
        shortlisted_spaces_id = request.query_params.get("shortlisted_spaces_id")
        requirements = Requirement.objects.filter(shortlisted_spaces_id=shortlisted_spaces_id)
        sectors = []
        verified_ops_user = {}
        for row in requirements:
            sectors.append(row.sector)

            if row.varified_ops_by and not verified_ops_user.get(row.varified_ops_by.id):
                verified_ops_user[row.varified_ops_by.id] = BaseUserSerializer(row.varified_ops_by,many=False).data
        requirement_obj = {}
        requirement_data = RequirementSerializer(requirements, many=True).data
        added_requirement = {}
        for row in requirement_data:
            key = str(row["lead_by"])+str(row["sub_sector"])+str(row["sector"])
            if added_requirement.get(key):
                continue

            if not requirement_obj.get(row["sector"]):
                requirement_obj[row["sector"]] = dict(row)
                requirement_obj[row["sector"]]["requirements"] = []

            row["verified_ops_by_obj"] = verified_ops_user.get(row["varified_ops_by"])

            requirement_obj[row["sector"]]["requirements"].append(row)

            added_requirement[key] = True

        companies = Organisation.objects.filter(business_type__in=sectors)
        companies_data = OrganisationSerializer(companies, many=True).data
        
        return ui_utils.handle_response({}, data={"requirements": requirement_obj, "companies": companies_data}, success=True)

    def put(self, request):
        requirements = request.data.get("requirements")
        for req in requirements:
            update_req = {
                "current_company": req["current_company"],
                "current_company_other": req["current_company_other"],
                "preferred_company": req["preferred_company"],
                "preferred_company_other": req["preferred_company_other"],
                "impl_timeline": req["impl_timeline"],
                "meating_timeline": req["meating_timeline"],
                "lead_status": req["lead_status"],
                "comment": req["comment"],
                "current_patner_feedback": req["current_patner_feedback"],
                "current_patner_feedback_reason": req["current_patner_feedback_reason"]
            }

            reqs = Requirement.objects.filter(
                sector_id = req["sector"], 
                sub_sector_id = req["sub_sector"], 
                shortlisted_spaces_id = req["shortlisted_spaces"], 
                lead_by_id = req["lead_by"]["id"],
            )
            for row in reqs:
                requirement_data = RequirementSerializer(row, data=update_req)

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

                    shortlisted_spaces = requirement.shortlisted_spaces
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
                    return ui_utils.handle_response({}, data={"error":"No campaigns available of lead distribution type of "+requirement.company.name+"."}, success=True)
        if shortlisted_spaces:
            requirement_exist = Requirement.objects.filter(shortlisted_spaces_id=shortlisted_spaces.id, varified_bd = "no", is_deleted = "no").first()
            if not requirement_exist:
                browsed_leads = BrowsedLead.objects.raw({"shortlisted_spaces_id":shortlisted_spaces.id, "status":"closed"}).values()
                if not dict(browsed_leads):
                    shortlisted_spaces.color_code = 3
                    shortlisted_spaces.save()

            
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
        phone_numers = [row["phone_number"] for row in browsed_leads]

        contact_details = ContactDetails.objects.filter(Q(mobile__in=phone_numers)|Q(landline__in=phone_numers))
        contact_details_dict_mobile = {str(row.mobile):row.name for row in contact_details}
        contact_details_dict_landline = {str(row.landline):row.name for row in contact_details}

        list1 = []
        for row in browsed_leads:
            row1 = dict(row)
            row1["_id"] = str(row1["_id"])

            row1["lead_by_name"] = contact_details_dict_mobile.get(row1["phone_number"])

            if not row1["lead_by_name"]:
                row1["lead_by_name"] = contact_details_dict_landline.get(row["phone_number"])

            list1.append(row1)

        return ui_utils.handle_response({}, data=list1, success=True)

class BrowsedLeadDelete(APIView):

    def post(self, request):
        browsed_ids = request.data.get("browsed_ids")

        for browsed_id in browsed_ids:
            mongo_client.browsed_lead.update({"_id": ObjectId(browsed_id)}, {"$set":{"status":"deleted"}})

        return ui_utils.handle_response({}, data="", success=True)

class DeleteRequirement(APIView):

    def post(self, request):
        requirement_ids = request.data.get('requirement_ids')

        requirements = Requirement.objects.filter(id__in=requirement_ids)

        for req in requirements:
            Requirement.objects.filter(sector=req.sector, sub_sector=req.sub_sector, shortlisted_spaces=req.shortlisted_spaces, lead_by=req.lead_by, is_deleted="no").update(is_deleted="yes")

        return ui_utils.handle_response({}, data="Requirement deleted", success=True)


class RestoreRequirement(APIView):
    # Requirement restore api (deletion revert api)

    def post(self, request):
        requirement_ids = request.data.get('requirement_ids')

        requirements = Requirement.objects.filter(id__in=requirement_ids)

        for req in requirements:
            Requirement.objects.filter(sector=req.sector, sub_sector=req.sub_sector, shortlisted_spaces=req.shortlisted_spaces, lead_by=req.lead_by, is_deleted="yes").update(is_deleted="no")

        return ui_utils.handle_response({}, data="Requirement restored", success=True)
        
class LeadOpsVerification(APIView):

    def post(self, request):
        requirement_ids = request.data.get("requirement_ids")
        requirements = Requirement.objects.filter(id__in=requirement_ids)
        for req in requirements:
            reqs = Requirement.objects.filter(sector=req.sector, sub_sector=req.sub_sector, shortlisted_spaces=req.shortlisted_spaces, lead_by=req.lead_by, is_deleted="no")
            for requirement in reqs:
                if requirement.varified_ops == "no":
                    requirement.varified_ops = "yes"
                    requirement.varified_ops_date = datetime.datetime.now()
                    requirement.varified_ops_by = request.user
                    requirement.save()
        return ui_utils.handle_response({}, data={}, success=True)

class BrowsedToRequirement(APIView):

    def post(self, request):
        browsed_ids = request.data.get("browsed_ids")
    
        shortlisted_spaces_id = None

        for browsed_id in browsed_ids:
            browsed = dict(mongo_client.browsed_lead.find_one({"_id": ObjectId(browsed_id)}))
            if browsed:
                mongo_client.browsed_lead.update({"_id": ObjectId(browsed_id)}, {"$set":{"status":"converted"}})

                companies = Organisation.objects.filter(business_type=browsed["sector_id"])
                
                contact_details = None
                if browsed["phone_number"]:
                    contact_details = ContactDetails.objects.filter(Q(mobile=browsed["phone_number"])|Q(landline=browsed["phone_number"])).first()
                
                prefered_patners_list = []
                if browsed["prefered_patners"]:
                    prefered_patners_list = Organisation.objects.filter(organisation_id__in=browsed["prefered_patners"]).all()
                
                shortlisted_spaces_id = browsed["shortlisted_spaces_id"]

                for company in companies:
                    requirement = Requirement(
                        campaign_id=browsed["campaign_id"],
                        shortlisted_spaces_id=browsed["shortlisted_spaces_id"],
                        company = company,
                        current_company_id = browsed["current_patner_id"],
                        is_current_patner = "yes" if browsed["current_patner_id"] == company.organisation_id else "no",
                        current_patner_feedback = browsed["current_patner_feedback"],
                        current_patner_feedback_reason = browsed["current_patner_feedback_reason"],
                        sector_id = browsed["sector_id"],
                        lead_by = contact_details,
                        impl_timeline = browsed["implementation_timeline"].lower(),
                        meating_timeline = browsed["meating_timeline"].lower(),
                        lead_status = browsed["lead_status"],
                        comment = browsed["comment"],
                        varified_ops = 'no',
                        varified_bd = 'no',
                        lead_date = datetime.datetime.now(),
                        preferred_company_other = browsed["prefered_patner_other"],
                        current_company_other = browsed["current_patner_other"],
                        l1_answers = browsed["l1_answers"],
                        l2_answers = browsed["l2_answers"],
                        sub_sector_id = browsed["sub_sector_id"]
                    )
                    requirement.save()

                    if prefered_patners_list:
                        requirement.preferred_company.set(prefered_patners_list)

        if shortlisted_spaces_id:
            ShortlistedSpaces.objects.filter(id=shortlisted_spaces_id).update(color_code=1, requirement_given='yes', requirement_given_date=datetime.datetime.now())

        return ui_utils.handle_response({}, data={}, success=True)


class BdVerification(APIView):

    def post(self, request):
        requirement_ids = request.data.get("requirement_ids")
        requirements = Requirement.objects.filter(id__in=requirement_ids)
        for req in requirements:
            reqs = Requirement.objects.filter(sector=req.sector, sub_sector=req.sub_sector, 
                shortlisted_spaces=req.shortlisted_spaces, lead_by=req.lead_by, is_deleted="no")
            if req.varified_ops == "no":
                for requirement in reqs:
                    requirement.varified_ops = "yes"
                    requirement.varified_ops_date = datetime.datetime.now()
                    requirement.varified_ops_by = request.user
                   
                    company_campaign = ProposalInfo.objects.filter(type_of_end_customer__formatted_name="b_to_b_l_d",
                     account__organisation=requirement.company).first()
                    if company_campaign:
                        company_shortlisted_space = requirement.shortlisted_spaces
                        if not company_shortlisted_space:
                            content_type = ui_utils.get_content_type(requirement.company_shortlisted_space.supplier_code)
                            center = ProposalCenterMapping.objects.filter(proposal=company_campaign).first()

                            company_shortlisted_space = ShortlistedSpaces(
                                proposal=company_campaign,
                                center=center,
                                supplier_code=requirement.company_shortlisted_space.supplier_code,
                                object_id=requirement.company_shortlisted_space.object_id,
                                content_type=content_type.data['data'],
                                status='F',
                                user=request.user,
                                requirement_given='yes',
                                requirement_given_date=datetime.datetime.now()
                            )
                            shortlisted_spaces.save()

                        requirement.company_campaign = company_campaign
                        requirement.company_shortlisted_spaces = company_shortlisted_space
                        requirement.save()

        return ui_utils.handle_response({}, data="Verified", success=True)