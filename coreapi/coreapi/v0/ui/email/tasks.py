from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from django.core.mail import EmailMessage
from models import EmailSettings
from v0.ui.leads.views import get_leads_excel_sheet
from v0.ui.leads.models import LeadsForm
from v0.ui.campaign.models import CampaignAssignment
from v0.ui.proposal.models import ProposalInfo
from views import send_mail_with_attachment
from v0.ui.proposal.views import get_supplier_list_by_status_ctrl
import datetime
import os
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

def send_weekly_leads_email():
    email_settings = EmailSettings.objects.filter(email_type="WEEKLY_LEADS").values("user__email", "is_allowed", "last_sent").all()
    email_settings_dict = {}
    for email_setting in email_settings:
        if email_setting["user__email"]:
            email_settings_dict[email_setting["user__email"]] = {"is_allowed": email_setting["is_allowed"], "last_sent": email_setting["last_sent"]}
    all_leads_forms = LeadsForm.objects.values('id', 'campaign_id').all()
    all_campaign_id_list = [leads_form['campaign_id'] for leads_form in all_leads_forms]
    all_campaign_assignment = CampaignAssignment.objects.filter(campaign_id__in=all_campaign_id_list).values('campaign_id', 'assigned_to__email').all()
    campaign_assignement_by_campaign_id = {}
    all_campaign_name = ProposalInfo.objects.filter(proposal_id__in=all_campaign_id_list).values('proposal_id', 'name')
    all_campaign_name_dict = {campaign['proposal_id']: campaign['name'] for campaign in all_campaign_name}
    for campaign_assignement in all_campaign_assignment:
        if campaign_assignement['campaign_id'] not in campaign_assignement_by_campaign_id:
            campaign_assignement_by_campaign_id[campaign_assignement['campaign_id']] = []
        if campaign_assignement['assigned_to__email'] not in email_settings_dict:
            continue
        if email_settings_dict[campaign_assignement['assigned_to__email']]['is_allowed']:
            campaign_assignement_by_campaign_id[campaign_assignement['campaign_id']].append(campaign_assignement['assigned_to__email'])
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=5)
    for leads_form in all_leads_forms:
        (book, total_leads_count) = get_leads_excel_sheet(leads_form['id'], 'All',start_date=start_date, end_date=None)
        if total_leads_count > 0:
            cwd = os.path.dirname(os.path.realpath(__file__))
            filename = 'leads_sheet_' + str(all_campaign_name_dict[leads_form['campaign_id']]) + '_' + str(start_date) + '_' + str(end_date) + '.xlsx'
            filepath = cwd + '/' + filename
            book.save(filepath)
            # to_array = campaign_assignement_by_campaign_id[leads_form['campaign_id']]
            # to_array = ["kshitij.mittal01@gmail.com"]
            # if len(to_array) != 0:
            #     send_mail_with_attachment(filepath, "Weekly Leads Data", to_array)
    return


class SendWeeklyLeadsMail(APIView):
    def get(self, request):
        send_weekly_leads_email()
        return ui_utils.handle_response('', data={}, success=True)


class SendGraphPdf(APIView):
    @staticmethod
    def post(request):
        file = request.data['file']
        campaign_id = request.data['campaign_id']
        campaign_assignment = CampaignAssignment.objects.filter(campaign_id=campaign_id).values(
            'campaign_id', 'assigned_to__email').all()
        # to_array = [x['assigned_to__email'] for x in campaign_assignment]
        to_array = ["kshitij.mittal01@gmail.com"]
        email = EmailMessage("test_sub", "test_bod", to=to_array)
        all_campaign_name = ProposalInfo.objects.filter(proposal_id=campaign_id).values('proposal_id','name')
        all_campaign_name_dict = {campaign['proposal_id']: campaign['name'] for campaign in all_campaign_name}
        filename = 'leads_graph_' + str(all_campaign_name_dict[campaign_id]) + '_' + str(datetime.datetime.now().date()) + '.pdf'
        email.attach(filename, file.read(), 'application/pdf')
        email.send()
        return ui_utils.handle_response('', data={}, success=True)


class SendBookingDetailMails(APIView):
    @staticmethod
    def get(request):
        supplier_list_details_by_status = get_supplier_list_by_status_ctrl("BYJMACF554")
        booking_template = get_template('booking_details.html')
        html = booking_template.render({'campaign_name': "test name", "details_list": supplier_list_details_by_status})
        to_array = ["kshitij.mittal01@gmail.com"]
        email = EmailMultiAlternatives('Subject', "some content")
        email.attach_alternative(html, "text/html")
        email.to = to_array
        email.send()
        return ui_utils.handle_response('', data={}, success=True)