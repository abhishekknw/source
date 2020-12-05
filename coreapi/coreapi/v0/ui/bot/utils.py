from v0.ui.account.models import ContactDetails, BusinessTypes, BusinessSubTypes
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, ProposalCenterMapping
import v0.ui.utils as ui_utils
import v0.ui.b2b.utils as b2b_utils
import datetime
from v0.ui.b2b.models import (Requirement, SuspenseLead, BrowsedLead)
from v0.ui.organisation.models import Organisation
from v0.ui.common.models import mongo_client
from django.db.models import Q

def bot_to_requirement(request, data):

    phone_number = data.get("phone")
    sessionIds = data.get("sessionIds")
    requestId = data.get("requestId")
    date_time = data.get("datetime")
    lead_status = "Lead"

    # if phone_number is None:
    #     return ui_utils.handle_response({}, data={"errors":"Sector \
    #         or Phone Number should not be null"}, success=False)

    contact_details = None
    if phone_number:
        contact_details = ContactDetails.objects.filter(
            Q(mobile=phone_number)|Q(landline=phone_number)).first()

    for row in data["data"]:
        sector_name = row.get("service")
        if sector_name:

            sub_sector_name = row.get("subservice")
            impl_timeline = row.get("implementationTime")
            meating_timeline = row.get("meetingTime")
            comment = "this is the test"
            current_patner = row.get("existingPartner")
            current_patner_feedback = row.get("partnerFeedback")
            current_patner_feedback_reason = row.get("feedbackReason")
            prefered_patners = row.get("preferredPartner")

            prefered_patners_array = []
            if prefered_patners:
                prefered_patners_split = prefered_patners.split(",")
                prefered_patners_array = [row.strip() for row in prefered_patners_split]

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

            submitted = "no"
            if meating_timeline:
                submitted = "yes"
            
            l1_answers = row.get("L1Response_1")
            l2_answers = row.get("L2Response_1")
            change_current_patner = "no"
            if current_patner_feedback == "Dissatisfied" or current_patner_feedback == "Extremely Dissatisfied":
                change_current_patner = "yes"

            supplier_id = ""
            supplier_type = "RS"
            sector = None
            if sector_name is not None:

                sector = BusinessTypes.objects.filter(
                    business_type=sector_name.lower()).first()

         
            
            sub_sector = None
            if sub_sector_name is not None:
                sub_sector = BusinessSubTypes.objects.filter(
                    business_sub_type=sub_sector_name.lower()).first()
            
            supplier = None
            city = None
            area = None
            supplier_name = None
            if contact_details:
                
                supplier_id = contact_details.object_id
                supplier = SupplierTypeSociety.objects.filter(
                    supplier_id=supplier_id).first()
                if supplier:
                    supplier_name = supplier.society_name
                    city = supplier.society_city
                    area = supplier.society_locality

                else:
                    supplier = SupplierMaster.objects.filter(
                        supplier_id=supplier_id).first()

                    if supplier:
                        supplier_type = supplier.supplier_type
                        city = supplier.city
                        area = supplier.area
                        supplier_name = supplier.supplier_name

            if supplier:
                
                campaign = ProposalInfo.objects.filter(Q(type_of_end_customer__formatted_name="b_to_b_r_g") & Q(name=area) | Q(name=city)).first()

                campaign_id = campaign.proposal_id

                shortlisted_spaces = ShortlistedSpaces.objects.filter(
                    proposal_id=campaign_id, object_id=supplier_id).first()

                if not shortlisted_spaces:
                    content_type = ui_utils.get_content_type(supplier_type)
                    center = ProposalCenterMapping.objects.filter(
                        proposal_id=campaign_id).first()

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
                    current_patner_obj = Organisation.objects.filter(
                        name=current_patner).first()
                    if not current_patner_obj:
                        current_company_other = current_patner

                if submitted and submitted.lower() == "yes":
                    shortlisted_spaces.color_code = 1
                    shortlisted_spaces.save()

                    companies = Organisation.objects.filter(business_type=sector)
                    for company in companies:
                        
                        lead_status = b2b_utils.get_lead_status(
                            impl_timeline = impl_timeline.lower(),
                            meating_timeline = meating_timeline.lower(),
                            company=company,
                            prefered_patners=prefered_patners_list,
                            change_current_patner=change_current_patner.lower()
                            )

                        
                        requirement = Requirement.objects.filter(sector=sector,campaign_id = campaign_id, sub_sector = sub_sector, is_deleted='no').first()
                        if not requirement:

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
                                l2_answers = l2_answers,
                                change_current_patner = change_current_patner.lower()
                            )
                            requirement.save()

                            if prefered_patners_list:
                                requirement.preferred_company.set(prefered_patners_list)
                        else:
                            requirement.sector = sector
                            requirement.sub_sector = sub_sector
                            requirement.shortlisted_spaces = shortlisted_spaces
                            requirement.company = company
                            requirement.current_company = current_patner_obj
                            requirement.current_company_other = current_company_other
                            requirement.is_current_patner = "yes" if current_patner_obj == company else "no"
                            requirement.current_patner_feedback = current_patner_feedback
                            requirement.current_patner_feedback_reason = current_patner_feedback_reason
                            requirement.preferred_company_other = preferred_company_other
                            requirement.impl_timeline = impl_timeline.lower()
                            requirement.meating_timeline = meating_timeline.lower()
                            requirement.lead_status = lead_status
                            requirement.lead_date = datetime.datetime.now()
                            requirement.l1_answers = l1_answers
                            requirement.l2_answers = l2_answers
                            requirement.change_current_patner = change_current_patner.lower()
                            requirement.comment = comment
                            requirement.save()

                            if prefered_patners_list:
                                requirement.preferred_company.set(prefered_patners_list)
                else:
                    if shortlisted_spaces.color_code != 1:
                        shortlisted_spaces.color_code = 2
                        shortlisted_spaces.save()
             
                    browse = mongo_client.browsed_lead.find({"sub_sector_id":str(sub_sector.id),"sector_id":str(sector.id)})
                    print(list(browse))
                    print(str(phone_number))
                    if not browse:

                        BrowsedLead(
                            supplier_id=supplier_id,
                            shortlisted_spaces_id=shortlisted_spaces.id,
                            campaign_id=campaign_id,
                            supplier_name = supplier_name,
                            city = city,
                            area = area,
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
                        mongo_client.BrowsedLead.update_one({"sector_id": sector.id,
                            "sub_sector_id": sub_sector.id},{"$set": {
                            "supplier_id" : supplier_id,
                            "shortlisted_spaces_id" : shortlisted_spaces.id,
                            "campaign_id" : campaign_id,
                            "phone_number" : phone_number,
                            "supplier_name" : supplier_name,
                            "city" : city,  
                            "area" : area,
                            "sector_id": sector.id,
                            "sub_sector_id": sub_sector.id,
                            "implementation_timeline": impl_timeline.lower(),
                            "meating_timeline": meating_timeline.lower(),
                            "lead_status" : lead_status,
                            "comment" : comment,
                            "current_patner_id" : current_patner_obj.organisation_id if current_patner_obj else None,
                            
                            "current_patner_other" : current_company_other,
                            "current_patner_feedback"  : current_patner_feedback,
                            "current_patner_feedback_reason" : current_patner_feedback_reason,
                            "prefered_patners" : prefered_patners_id_list,
                            "prefered_patner_other": preferred_company_other,
                            
                            "l1_answers":l1_answers,
                            "l2_answers":l2_answers,
                        }})

                        
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

        else:
            pass
    return ui_utils.handle_response({}, data={}, success=True)