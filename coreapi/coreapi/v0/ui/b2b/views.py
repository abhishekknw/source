from __future__ import print_function
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (Requirement)
import v0.ui.utils as ui_utils
from openpyxl import load_workbook
from v0.ui.account.models import ContactDetails
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, ProposalCenterMapping
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
                phone_number = get_value_from_list_by_key(row, headers.get('phone number'))
                
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
                        
                        # Requirement(
                        #     campaign=campaign,
                        #     shortlisted_spaces=shortlisted_spaces,
                        #     company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='company')
                        #     current_company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='current')
                        #     preferred_company = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE, related_name='preferred')
                        #     sector = models.ForeignKey('BusinessTypes', null=True, blank=True, on_delete=models.CASCADE)
                        #     sub_sector = models.ForeignKey('BusinessSubTypes', null=True, blank=True, on_delete=models.CASCADE)
                        #     lead_by = models.ForeignKey('ContactDetails', null=True, blank=True, on_delete=models.CASCADE)
                        #     impl_timeline = models.CharField(max_length=30, choices=IMPL_TIMELINE_CATEGORY, default=IMPL_TIMELINE_CATEGORY[1][0]) # implementation_timeline
                        #     meating_timeline = models.CharField(max_length=30, choices=MEATING_TIMELINE_CATEGORY, default=MEATING_TIMELINE_CATEGORY[1][0]) # meating_timeline
                        #     lead_status = models.CharField(max_length=30, choices=LEAD_STATUS_CATEGORY, default=LEAD_STATUS_CATEGORY[1][0])
                        #     comment = models.TextField(max_length=500, blank=True)
                        #     varified = models.CharField(max_length=5, choices=(("yes","yes"),("no","no")), default="no")
                        #     created_at = models.DateTimeField(auto_now_add=True)
                        #     updated_at = models.DateTimeField(auto_now=True)
                        # ).save()

                else:
                    pass
        
        return ui_utils.handle_response({}, data={}, success=True)