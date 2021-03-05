from .models import Requirement,NotificationTemplates,PreRequirement,BrowsedLead
import requests
from openpyxl import load_workbook, Workbook
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
from v0.ui.account.models import ContactDetails, BusinessTypes, BusinessSubTypes


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
            req.lead_by.name,
            req.call_back_preference,
            req.lead_date,
            "yes",
            "no",
            req.varified_ops,
            req.is_deleted
        ]

        sheet.append(row2)

    for browsed in browsed_leads:
        
        index = index + 1
        sector = BusinessTypes.objects.filter(id=browsed['sector_id']).first()
        sub_sector = BusinessSubTypes.objects.filter(id=browsed['sub_sector_id']).first()

        try:
            supplier_type = None
            supplier_type = browsed['supplier_type']
        except Exception as e:
            supplier_type = None

        row3 = [
            index,
            browsed['supplier_id'],
            browsed['supplier_name'],
            supplier_type,
            browsed['area'],
            browsed['city'],
            sector.business_type if sector.business_type else None,
            sub_sector.business_sub_type if sub_sector else None,
            browsed['current_patner_id'],
            browsed['current_patner_other'],
            browsed['current_patner_feedback'],
            ", ".join(browsed['prefered_patners']),
            browsed['prefered_patner_other'],

            browsed['l1_answers'],
            browsed['l1_answer_2'],
            browsed['l2_answers'],
            browsed['l2_answer_2'],

            browsed['implementation_timeline'],
            browsed['meating_timeline'],
            browsed['lead_status'],

            browsed['comment'],
            None,
            browsed['call_back_preference'],
            browsed['created_at'],
            "no",
            "yes",
            "no",
            "no"
        ]   
        sheet.append(row3)

    return book
