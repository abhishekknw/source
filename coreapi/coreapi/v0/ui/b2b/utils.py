from .models import Requirement,NotificationTemplates,PreRequirement,BrowsedLead
import requests
from openpyxl import load_workbook, Workbook
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
from v0.ui.account.models import ContactDetails, BusinessTypes, BusinessSubTypes
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.organisation.models import Organisation


def get_lead_status(impl_timeline,meating_timeline,prefered_patners,
	company,change_current_patner):
	
	prefered_patner = "no"
	if prefered_patners:
		prefered_patner = "yes"

	if change_current_patner == "yes":
		if impl_timeline == "within 2 weeks" and prefered_patner == "yes":
			return "Deep Lead"
		elif impl_timeline == "within 2 weeks" and meating_timeline == "as soon as possible" \
			and prefered_patner == "no":
			return "Hot Lead"
		elif (impl_timeline == "within 2 weeks" and meating_timeline is not "as soon as possible" \
			and prefered_patner == "no") or (impl_timeline is not "within 2 weeks" and  \
			meating_timeline == "as soon as possible" and prefered_patner == "yes"):
			return "Warm Lead"
		else:
			return "Lead"
	else:
		return "Raw Lead"

def send_whatsapp_notification(company,notification_type,destination):
	
	API_ENDPOINT = "http://35.226.184.99:5002/v1/message/push/94d3874500a84f87cf63e14007f7cfa2"

	# contact_details = SalesRepresentatives.objects.filter(company=company).first()
	template = NotificationTemplates.objects.filter(notification_type=
		notification_type).first()

	if template:

		data = {
		 "destination": destination,
		 "message" :template.content
		}
		
		# sending post request and saving response as response object 
		rspnse = requests.post(url = API_ENDPOINT, data = data)

		# extracting response text  
		pastebin_url = rspnse.text

	return True

def get_color_code(shortlisted_spaces_id):
    
    requirement = PreRequirement.objects.filter(shortlisted_spaces_id=shortlisted_spaces_id)
    browsed_leads = list(BrowsedLead.objects.raw(
        {"shortlisted_spaces_id":str(shortlisted_spaces_id),
        "status":"closed"}))
    color_code_list = []

    if requirement:

        for req in requirement:

            if req.varified_ops == "no" and req.is_deleted == "no":
                color_code_list.append(1) # Yellow
            elif req.varified_ops == "yes" and req.is_deleted == "no":
                if browsed_leads:
                    color_code_list.append(2) # Brown
                else:
                    color_code_list.append(3) # Green
            elif req.is_deleted == "yes":
                color_code_list.append(5) # Green
            else:
                if browsed_leads:
                    color_code_list.append(2) # Brown
                else:
                    color_code_list.append(4) # Green

        if 1 in color_code_list:
            color_code = 1 #Yellow
        else:
            if 2 in color_code_list:
                color_code = 2 #Brown
            else:
                if 3 in color_code_list:
                    color_code = 3 #Green 
                else:
                    color_code = 4 #White
    else:
        if browsed_leads:
            color_code = 2 #Brown
        else:
            color_code = 4 #White

    shortlisted_spac = ShortlistedSpaces.objects.filter(id=shortlisted_spaces_id).first()
    shortlisted_spac.color_code = color_code
    shortlisted_spac.save()

    return color_code

def download_b2b_leads(requirement,browsed_leads):
	
    header_list = ['Index','Supplier Id','Supplier Name','Supplier Type','Area',
        'City','Sector','Sub Sector','Current Partner','Current Partner Other','FeedBack',
        'Preferred Partner','Preferred Partner Other','L1 Answer 1 ','L1 Answer 2', 
        'L2 Answer 1','L2 Answer 2','Implementation Time','Meeting Time','Lead Status',
        'Comment','Lead Given by','Call Back Time','Timestamp','Submitted','Browsed',
        'Ops Verified','Deleted' 
        
    ]

    book = Workbook()
    sheet = book.active
    sheet.append(header_list)
    index = 0
    lead_data = []

    for req in requirement:

        supplier_data = SupplierTypeSociety.objects.filter(
            supplier_id=req.shortlisted_spaces.object_id).first()

        if supplier_data:
            supplier_type = "RS"
            supplier_name = supplier_data.society_name
            city = supplier_data.society_city
            area = supplier_data.society_locality

        if supplier_data is None:
            supplier_data = SupplierMaster.objects.filter(
                supplier_id=req.shortlisted_spaces.object_id).first()
            
            supplier_type = supplier_data.supplier_type
            city = supplier_data.city
            area = supplier_data.area
            supplier_name = supplier_data.supplier_name

        index = index + 1

        preferred_company = None
        preferred_company_list = req.preferred_company.all()
        company_list = []
        if preferred_company_list:
            for row in preferred_company_list:
                company_list.append(row.name)
        preferred_company = ", ".join(company_list)

        row2 = [
            index,
            req.shortlisted_spaces.object_id,
            supplier_name,
            supplier_type,
            area,
            city,
            req.sector.business_type if req.sector else None,
            req.sub_sector.business_sub_type if req.sub_sector else None,
            req.current_company.name if req.current_company else None,
            req.current_company_other,
            req.current_patner_feedback,
            preferred_company,
            req.preferred_company_other,
            req.l1_answers,
            req.l1_answer_2,
            req.l2_answers,
            req.l2_answer_2,
            req.impl_timeline,
            req.meating_timeline,
            req.lead_status,
            req.comment,
            req.lead_by.name if req.lead_by else None,
            req.call_back_preference,
            req.lead_date,
            "yes",
            "no",
            req.varified_ops,
            req.is_deleted
        ]

        sheet.append(row2)

    if browsed_leads:
        
        for browsed in browsed_leads:
            
            index = index + 1
            try:
                b_sector_id = browsed['sector_id']
                b_sector = BusinessTypes.objects.filter(id=b_sector_id).first()
            except Exception as e:
                b_sector = None

            try:
                b_sub_sector_id = browsed['sub_sector_id']
                b_sub_sector = BusinessSubTypes.objects.filter(id=b_sub_sector_id).first()
            except Exception as e:
                b_sub_sector = None

            try:
                b_supplier_type = browsed['supplier_type']
            except Exception as e:
                b_supplier_type = None

            try:
                b_l1_answers = browsed['l1_answers']
            except Exception as e:
                b_l1_answers = None

            try:
                b_l1_answer_2 = browsed['l1_answer_2']
            except Exception as e:
                b_l1_answer_2 = None

            try:
                b_l2_answers = browsed['l2_answers']
            except Exception as e:
                b_l2_answers = None

            try:
                b_l2_answer_2 = browsed['l2_answer_2']
            except Exception as e:
                b_l2_answer_2 = None

            try:
                b_implementation_timeline = browsed['implementation_timeline']
            except Exception as e:
                b_implementation_timeline = None

            try:
                b_meating_timeline = browsed['meating_timeline']
            except Exception as e:
                b_meating_timeline = None

            try:
                b_call_back_preference = browsed['call_back_preference']
            except Exception as e:
                b_call_back_preference = None

            try:
                b_prefered_patner_other = browsed['prefered_patner_other']
            except Exception as e:
                b_prefered_patner_other = None

            try:
                b_current_patner_feedback = browsed['current_patner_feedback']
            except Exception as e:
                b_current_patner_feedback = None

            try:
                b_current_patner_other = browsed['current_patner_other']
            except Exception as e:
                b_current_patner_other = None

            try:
                b_current_patner_id = browsed['current_patner_id']
            except Exception as e:
                b_current_patner_id = None

            try:
                b_supplier_name = browsed['supplier_name']
            except Exception as e:
                b_supplier_name = None

            try:
                b_supplier_id = browsed['supplier_id']
            except Exception as e:
                b_supplier_id = None

            try:
                b_area = browsed['area']
            except Exception as e:
                b_area = None

            try:
                b_city = browsed['city']
            except Exception as e:
                b_city = None

            try:
                b_comment = browsed['comment']
            except Exception as e:
                b_comment = None

            try:
                b_prefered_patners = browsed['prefered_patners']
            except Exception as e:
                b_prefered_patners = None

            b_current_patner = Organisation.objects.filter(
                organisation_id=b_current_patner_id).first()

            b_prefered_patners_list = Organisation.objects.filter(
                organisation_id__in=b_prefered_patners).all()

            b_preferred_company = None
            b_company_list = []
            if b_prefered_patners_list:
                for b_row in b_prefered_patners_list:
                    b_company_list.append(b_row.name)
            b_preferred_company = ", ".join(b_company_list)

            row3 = [
                index,
                b_supplier_id,
                b_supplier_name,
                b_supplier_type,
                b_area,
                b_city,
                b_sector.business_type if b_sector else None,
                b_sub_sector.business_sub_type if b_sub_sector else None,
                b_current_patner.name if b_current_patner else None,
                b_current_patner_other,
                b_current_patner_feedback,
                b_preferred_company,
                b_prefered_patner_other,

                b_l1_answers,
                b_l1_answer_2,
                b_l2_answers,
                b_l2_answer_2,

                b_implementation_timeline,
                b_meating_timeline,
                None,

                b_comment,
                None,
                b_call_back_preference,
                browsed['created_at'],
                "no",
                "yes",
                "no",
                "no"
            ]   
            sheet.append(row3)

    return book
