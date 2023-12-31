from __future__ import absolute_import
from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from django.core.mail import EmailMessage
from .models import EmailSettings
from v0.ui.leads.views import get_leads_excel_sheet
from v0.ui.campaign.models import CampaignAssignment
from v0.ui.proposal.models import ProposalInfo
from v0.ui.proposal.views import get_supplier_list_by_status_ctrl
import datetime
from datetime import timedelta
import os
import json
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from v0.ui.common.models import mongo_client
from v0.ui.proposal.views import convert_date_format
from .views import send_email, send_mail_generic
from v0.ui.common.models import BaseUser
from celery import shared_task
from django.conf import settings
from v0.ui.proposal.models import SupplierPhase
DEFAULT_CC_EMAILS = settings.DEFAULT_CC_EMAILS


def get_all_campaign_assignment_by_id(email_type):
    email_settings = EmailSettings.objects.filter(email_type=email_type).values("user__email", "is_allowed",
                                                                                    "last_sent", "user_type").all()
    email_settings_dict = {}
    for email_setting in email_settings:
        if email_setting["user__email"]:
            email_settings_dict[email_setting["user__email"]] = {"is_allowed": email_setting["is_allowed"],
                                                                 "last_sent": email_setting["last_sent"],
                                                                 "user_type": email_setting["user_type"]}
    all_leads_forms = list(mongo_client.leads_forms.find())
    all_campaign_assignment = CampaignAssignment.objects.values(
        'campaign_id', 'assigned_to__email').all()
    all_campaign_id_list = [campaign_assignment['campaign_id'] for campaign_assignment in all_campaign_assignment]
    campaign_assignement_by_campaign_id = {}
    campaign_assignement_by_campaign_id_admins = {}
    all_campaign_name = ProposalInfo.objects.filter(proposal_id__in=all_campaign_id_list).values('proposal_id', 'name')
    all_campaign_name_dict = {campaign['proposal_id']: campaign['name'] for campaign in all_campaign_name}
    for campaign_assignement in all_campaign_assignment:
        if campaign_assignement['campaign_id'] not in campaign_assignement_by_campaign_id:
            campaign_assignement_by_campaign_id[campaign_assignement['campaign_id']] = []
            campaign_assignement_by_campaign_id_admins[campaign_assignement['campaign_id']] = []
        if campaign_assignement['assigned_to__email'] not in email_settings_dict:
            continue
        if email_settings_dict[campaign_assignement['assigned_to__email']]['is_allowed']:
            campaign_assignement_by_campaign_id[campaign_assignement['campaign_id']].append(
                campaign_assignement['assigned_to__email'])
            if email_settings_dict[campaign_assignement['assigned_to__email']]['user_type'] == 'ADMIN':
                campaign_assignement_by_campaign_id_admins[campaign_assignement['campaign_id']].append(
                    campaign_assignement['assigned_to__email'])
    return (campaign_assignement_by_campaign_id, campaign_assignement_by_campaign_id_admins, all_leads_forms, all_campaign_name_dict)


def send_weekly_leads_email():
    (campaign_assignement_by_campaign_id, campaign_assignement_by_campaign_id_admins, all_leads_forms,
     all_campaign_name_dict) = get_all_campaign_assignment_by_id("WEEKLY_LEADS")
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=7)
    for leads_form in all_leads_forms:
        (book, total_leads_count) = get_leads_excel_sheet(leads_form['leads_form_id'], 'All',start_date=start_date, end_date=end_date)
        if total_leads_count > 0:
            cwd = os.path.dirname(os.path.realpath(__file__))
            filename = 'leads_sheet_' + str(all_campaign_name_dict[leads_form['campaign_id']]) + '_' + str(start_date) + '_' + str(end_date) + '.xlsx'
            filepath = cwd + '/' + filename
            book.save(filepath)
            leads_template = get_template('weekly_leads.html')
            html_body = leads_template.render({'campaign_name': str(all_campaign_name_dict[leads_form['campaign_id']])})
            to_array = campaign_assignement_by_campaign_id[leads_form['campaign_id']]
            if len(to_array) != 0:
                send_mail_generic.delay("Weekly Leads Data", to_array,html_body, None, filepath)
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
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        if start_date and end_date:
            start_date = datetime.datetime.strptime(str(start_date),"%Y-%m-%d").strftime("%d-%b-%Y")
            end_date = datetime.datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%d-%b-%Y")
        (campaign_assignement_by_campaign_id, campaign_assignement_by_campaign_id_admins, all_leads_forms,
         all_campaign_name_dict) = get_all_campaign_assignment_by_id("WEEKLY_LEADS_GRAPH")
        to_array = campaign_assignement_by_campaign_id[campaign_id]
        all_campaign_name = ProposalInfo.objects.filter(proposal_id=campaign_id).values('proposal_id','name')
        all_campaign_name_dict = {campaign['proposal_id']: campaign['name'] for campaign in all_campaign_name}
        this_campaign_name = str(all_campaign_name_dict[campaign_id])
        filename = 'leads_graph_' + str(all_campaign_name_dict[campaign_id]) + '_' + str(datetime.datetime.now().date()) + '.pdf'
        self_leads_template = get_template('leads_graph_email.html')
        html_body = self_leads_template.render({'campaign_name': this_campaign_name})
        subject = "Leads Graphs from " + str(start_date) + " to " + str(end_date)
        email = EmailMultiAlternatives(subject, body=html_body, to=to_array)
        email.attach(filename, file.read(), 'application/pdf')
        email.content_subtype = 'html'
        email.send()
        return ui_utils.handle_response('', data={}, success=True)

@shared_task()
def send_booking_mails_ctrl(template_name,req_campaign_id=None, email=None):
    (campaign_assignement_by_campaign_id, campaign_assignement_by_campaign_id_admins, all_leads_forms,
     all_campaign_name_dict) = get_all_campaign_assignment_by_id("BOOKING_DETAILS_ADV")
    all_campaign_ids = list(set([lead_form['campaign_id'] for lead_form in all_leads_forms]))
    if req_campaign_id:
        all_campaign_ids = [req_campaign_id]
    for campaign_id in all_campaign_ids:
        supplier_list_details_by_status = get_supplier_list_by_status_ctrl(campaign_id)
        supplier_list_details_by_status = json.dumps(supplier_list_details_by_status)
        booking_template = get_template(template_name)
        to_array = emailToEmailList(email) if email else campaign_assignement_by_campaign_id[campaign_id]
        supplier_list_details_by_status_json = json.loads(supplier_list_details_by_status)
        html = booking_template.render(
            {"campaign_name": str(all_campaign_name_dict[campaign_id]),
             "details_dict": supplier_list_details_by_status_json})
        if template_name == 'pipeline_details.html':
            subject = "Suppliers In Pipeline For " + str(all_campaign_name_dict[campaign_id])
        elif template_name == 'pre_hype_emails.html':
            subject = "Suppliers In Pre-Hype For " + str(all_campaign_name_dict[campaign_id])
        elif template_name == 'recce_email.html':
            subject = "Suppliers In Recce For " + str(all_campaign_name_dict[campaign_id])
        elif template_name == 'booking_details.html':
            if len(supplier_list_details_by_status_json['upcoming_phases']) > 0:
                start_date = supplier_list_details_by_status_json['upcoming_phases'][0]['start_date']
                end_date = supplier_list_details_by_status_json['upcoming_phases'][0]['end_date']
            else:
                start_date = (datetime.datetime.now() + timedelta(days=1)).strftime('%d %b %Y')
                end_date = (datetime.datetime.now() + timedelta(days=4)).strftime('%d %b %Y')
            subject = "Suppliers for " + str(all_campaign_name_dict[campaign_id]) + ": " + start_date + " to " + end_date
        elif template_name == 'advanced_booking_details.html':
            if (supplier_list_details_by_status_json['ongoing_phase']):
                start_date = supplier_list_details_by_status_json['ongoing_phase']['start_date']
                end_date = supplier_list_details_by_status_json['ongoing_phase']['end_date']
            else:
                start_date = (datetime.datetime.now() + timedelta(days=1)).strftime('%d %b %Y')
                end_date = (datetime.datetime.now() + timedelta(days=4)).strftime('%d %b %Y')
            subject = str(all_campaign_name_dict[campaign_id]) + " Suppliers Activation Details for this Weekend (" + start_date + " to " + end_date + ")"
        elif template_name == 'daily_assignment_mail.html':
            subject = "Suppliers Assigned for " + str(all_campaign_name_dict[campaign_id])
            # Get assigned user
            campaign_assignment = CampaignAssignment.objects.filter(campaign_id=campaign_id)
            for campaign in campaign_assignment:
                user = BaseUser.objects.filter(id=campaign.assigned_to_id).values('email')
                to_array = []
                if user and len(user) > 0:
                    if user[0] and user[0]['email'] and user[0]['email'].find('machadalo') > -1:
                        to_array.append(user[0]['email'])
        send_mail_generic.delay(subject, to_array, html, None,None)
    return

#To split multiple emails by comma
def emailToEmailList(email):
    return email.split(',')

class SendBookingDetailMails(APIView):
    @staticmethod
    def get(request, campaign_id):
        email_id = request.query_params.get("email", None)
        send_booking_mails_ctrl('booking_details.html', campaign_id, email_id)
        return ui_utils.handle_response('', data={}, success=True)

class SendRecceMails(APIView):
    @staticmethod
    def get(request, campaign_id):
        email_id = request.query_params.get("email", None)
        send_booking_mails_ctrl('recce_email.html', campaign_id, email_id)
        return ui_utils.handle_response('', data={}, success=True)

class SendPreHypeMails(APIView):
    @staticmethod
    def get(request, campaign_id):
        email_id = request.query_params.get("email", None)
        send_booking_mails_ctrl('pre_hype_emails.html', campaign_id, email_id)
        return ui_utils.handle_response('', data={}, success=True)

class SendPipelineDetailMails(APIView):
    @staticmethod
    def get(request, campaign_id):
        email_id = request.query_params.get("email", None)
        send_booking_mails_ctrl('pipeline_details.html', campaign_id, email_id)
        return ui_utils.handle_response('', data={}, success=True)

class SendAdvancedBookingDetailMails(APIView):
    @staticmethod
    def get(request, campaign_id):
        email_id = request.query_params.get("email", None)
        send_booking_mails_ctrl('advanced_booking_details.html', campaign_id, email_id)
        return ui_utils.handle_response('', data={}, success=True)


class SendLeadsToSelf(APIView):
    @staticmethod
    def post(request):
        data = request.data
        start_date = None
        end_date = None
        if 'start_date' in data:
            start_date = data['start_date'][:10]
            start_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d').date()
        if 'end_date' in data:
            end_date = data['end_date'][:10]
            end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
        leads_form_id = data['leads_form_id']
        campaign_id = data['campaign_id']
        (campaign_assignement_by_campaign_id, campaign_assignement_by_campaign_id_admins, all_leads_forms,
         all_campaign_name_dict) = get_all_campaign_assignment_by_id("WEEKLY_LEADS")
        all_super_users = BaseUser.objects.filter(is_superuser=1).all()
        all_super_user_emailids = [user.email for user in all_super_users]
        user_email = request.user.email
        username = request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        campaign_name = str(all_campaign_name_dict[campaign_id])
        (book, total_leads_count) = get_leads_excel_sheet(leads_form_id, 'All', start_date=start_date, end_date=end_date)
        cwd = os.path.dirname(os.path.realpath(__file__))
        filename = 'leads_sheet_' +  campaign_name + '_' + str(
            start_date) + '_' + str(end_date) + '.xlsx'
        filepath = cwd + '/' + filename
        book.save(filepath)
        to_array = [user_email] if user_email in campaign_assignement_by_campaign_id[campaign_id] else []
        #to_array = ['kshitij.mittal01@gmail.com']
        if len(to_array) != 0:
            self_leads_template = get_template('self_leads_email.html')
            html_body = self_leads_template.render({'campaign_name': campaign_name, 'first_name':first_name,
                                               'last_name':last_name})
            send_mail_generic.delay("Custom Leads Data", to_array,html_body,None, filepath)
            to_array_admins = campaign_assignement_by_campaign_id_admins[campaign_id]
            to_array_admins = list(set(to_array_admins + all_super_user_emailids))
            if user_email in to_array_admins:
                to_array_admins.remove(user_email)
            # if len(to_array_admins) > 0:
            #     subject = 'Leads Custom Email Generation Alert!'
            #     body = 'User with username {0} and email {1} has generated a leads mail for campaign - {2} from date: {3} to date: {4}.'.format(username, user_email, campaign_name, str(start_date), str(end_date))
            #     send_mail_generic.delay(subject, to_array_admins, body, None, None)
        return ui_utils.handle_response('', data={}, success=True)


class SendDailyAssignmentMails(APIView):
    @staticmethod
    def get(request):
        # Get all ongoing campaigns
        current_date = datetime.datetime.now().date()
        phases = SupplierPhase.objects.filter(start_date__lte=current_date, end_date__gte=current_date).all()
        for phase in phases:
            campaign_id = phase.campaign_id
            send_booking_mails_ctrl('daily_assignment_mail.html', campaign_id)
        return ui_utils.handle_response('', data={}, success=True)