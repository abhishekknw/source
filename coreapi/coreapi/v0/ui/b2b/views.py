from __future__ import print_function
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (Requirement)
import v0.ui.utils as ui_utils
from openpyxl import load_workbook
from v0.ui.account.models import ContactDetails, BusinessTypes
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, ProposalCenterMapping
from v0.ui.organisation.models import Organisation
from django.db.models import Q
import v0.ui.utils as ui_utils
import datetime

def get_value_from_list_by_key(list1, key):
    try:
        return list1[key].value.strip()
    except:
        pass

class ImportLead(APIView):
    def get(self, request):
        return ui_utils.handle_response({}, data={}, success=True)

    def post(self, request):
        data = request.data.copy()
        source_file = data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        headers = {}

        campaign = ProposalInfo.objects.filter(type_of_end_customer__formatted_name="b_to_b_r_g").first()
        center = ProposalCenterMapping.objects.filter(proposal=campaign).first()
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
                sector_name = get_value_from_list_by_key(row, headers.get('sector'))
                impl_timeline = get_value_from_list_by_key(row, headers.get('implementation timeline'))
                meating_timeline = get_value_from_list_by_key(row, headers.get('meating timeline'))
                lead_status = get_value_from_list_by_key(row, headers.get('lead status'))
                comment = get_value_from_list_by_key(row, headers.get('comment'))
                current_patner = get_value_from_list_by_key(row, headers.get('current partner'))
                prefered_patners = get_value_from_list_by_key(row, headers.get('prefered partners'))
                
                contact_details = ContactDetails.objects.filter(Q(mobile=phone_number)|Q(landline=phone_number)).first()

                if contact_details:
                    supplier = SupplierTypeSociety.objects.filter(supplier_id=contact_details.object_id).first()
                    city = ""
                    area = ""
                    supplier_type = ""

                    if supplier:
                        city = supplier.society_city
                        area = supplier.society_locality
                        supplier_type = "RS"
                    else:
                        supplier = SupplierMaster.objects.filter(supplier_id=contact_details.object_id).first()

                        city = supplier.address_supplier.city
                        area = supplier.address_supplier.area
                        supplier_type = supplier.supplier_type
                    
                    if campaign:
                        shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id, object_id=contact_details.object_id).first()
                        if not shortlisted_spaces:

                            content_type = ui_utils.get_content_type(supplier_type)

                            shortlisted_spaces = ShortlistedSpaces(
                                proposal=campaign,
                                center=center,
                                supplier_code=supplier_type,
                                object_id=contact_details.object_id,
                                content_type=content_type.data['data'],
                                status='F',
                                user=request.user,
                                requirement_given='yes',
                                requirement_given_date=datetime.datetime.now()
                            )
                            shortlisted_spaces.save()
                        
                        sector = BusinessTypes.objects.filter(business_type=sector_name.lower()).first()
                        companies = Organisation.objects.filter(business_type=sector)

                        current_patner_obj = None
                        if current_patner:
                            current_patner_obj = Organisation.objects.filter(name=current_patner).first()

                        prefered_patners_list = []
                        if prefered_patners:
                            prefered_patners_split = prefered_patners.split(",")
                            prefered_patners_split = [row.strip() for row in prefered_patners_split]
                            prefered_patners_list = Organisation.objects.filter(name__in=prefered_patners_split).all()
                        
                        for company in companies:
                            requirement = Requirement(
                                campaign=campaign,
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
                                varified = 'no',
                                lead_date = datetime.datetime.now()
                            )
                            requirement.save()

                            if prefered_patners_list:
                                requirement.preferred_company.set(prefered_patners_list)

                else:
                    pass
        
        return ui_utils.handle_response({}, data={}, success=True)