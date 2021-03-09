from .models import Requirement,NotificationTemplates,PreRequirement,BrowsedLead
import requests
from openpyxl import load_workbook, Workbook
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
from v0.ui.account.models import ContactDetails, BusinessTypes, BusinessSubTypes
from v0.ui.proposal.models import ShortlistedSpaces


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
            sector = BusinessTypes.objects.filter(id=browsed['sector_id']).first()
            sub_sector = BusinessSubTypes.objects.filter(id=browsed['sub_sector_id']).first()

            try:
                supplier_type = browsed['supplier_type']
            except Exception as e:
                supplier_type = None

            try:
                l1_answers = browsed['l1_answers']
            except Exception as e:
                l1_answers = None

            try:
                l1_answer_2 = browsed['l1_answer_2']
            except Exception as e:
                l1_answer_2 = None

            try:
                l2_answers = browsed['l2_answers']
            except Exception as e:
                l2_answers = None

            try:
                l2_answer_2 = browsed['l2_answer_2']
            except Exception as e:
                l2_answer_2 = None

            try:
                implementation_timeline = browsed['implementation_timeline']
            except Exception as e:
                implementation_timeline = None

            try:
                meating_timeline = browsed['meating_timeline']
            except Exception as e:
                meating_timeline = None


            try:
                lead_status = browsed['lead_status']
            except Exception as e:
                lead_status = None

            try:
                call_back_preference = browsed['call_back_preference']
            except Exception as e:
                call_back_preference = None

            try:
                prefered_patner_other = browsed['prefered_patner_other']
            except Exception as e:
                prefered_patner_other = None

            try:
                current_patner_feedback = browsed['current_patner_feedback']
            except Exception as e:
                current_patner_feedback = None

            try:
                current_patner_other = browsed['current_patner_other']
            except Exception as e:
                current_patner_other = None

            try:
                current_patner_id = browsed['current_patner_id']
            except Exception as e:
                current_patner_id = None

            try:
                supplier_name = browsed['supplier_name']
            except Exception as e:
                supplier_name = None

            try:
                supplier_id = browsed['supplier_id']
            except Exception as e:
                supplier_id = None

            try:
                area = browsed['area']
            except Exception as e:
                area = None

            try:
                city = browsed['city']
            except Exception as e:
                city = None

            try:
                comment = browsed['comment']
            except Exception as e:
                comment = None

            try:
                prefered_patners = browsed['prefered_patners']
            except Exception as e:
                prefered_patners = None

            row3 = [
                index,
                supplier_id,
                supplier_name,
                supplier_type,
                area,
                city,
                sector.business_type if sector.business_type else None,
                sub_sector.business_sub_type if sub_sector else None,
                current_patner_id,
                current_patner_other,
                current_patner_feedback,
                ", ".join(prefered_patners),
                prefered_patner_other,

                l1_answers,
                l1_answer_2,
                l2_answers,
                l2_answer_2,

                implementation_timeline,
                meating_timeline,
                lead_status,

                comment,
                None,
                call_back_preference,
                browsed['created_at'],
                "no",
                "yes",
                "no",
                "no"
            ]   
            sheet.append(row3)

    return book
