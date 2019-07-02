from __future__ import absolute_import
from rest_framework.views import APIView
import v0.ui.utils as ui_utils
from django.core.mail import EmailMessage
from .models import EmailSettings
from v0.ui.leads.views import get_leads_excel_sheet
from v0.ui.campaign.models import CampaignAssignment
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces
from v0.ui.proposal.views import get_supplier_list_by_status_ctrl
import datetime
from datetime import timedelta
import os
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from v0.ui.common.models import mongo_client
from v0.ui.proposal.views import convert_date_format
from .views import send_email, send_mail_generic, send_mail_with_attachment
from v0.ui.common.models import BaseUser
from celery import shared_task
from django.conf import settings
DEFAULT_CC_EMAILS = settings.DEFAULT_CC_EMAILS
ENV = settings.ENV
import schedule
import time
from v0.ui.account.models import ContactDetails
import csv
from django.db import connection

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
        # to_array = ["yogesh.mhetre@machadalo.com"]
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
        supplier_list_details_by_status = supplier_list_details_by_status
        booking_template = get_template(template_name)
        to_array = [email] if email else campaign_assignement_by_campaign_id[campaign_id]
        
        html = booking_template.render(
            {'campaign_name': str(all_campaign_name_dict[campaign_id]),
             "details_dict": supplier_list_details_by_status})
        if template_name == 'pipeline_details.html':
            subject = "Socities In Pipeline For " + str(all_campaign_name_dict[campaign_id])
        elif template_name == 'booking_details.html':
            if len(supplier_list_details_by_status['upcoming_phases']) > 0:
                start_date = supplier_list_details_by_status['upcoming_phases'][0]['start_date']
                end_date = supplier_list_details_by_status['upcoming_phases'][0]['end_date']
            else:
                start_date = (datetime.datetime.now() + timedelta(days=1)).strftime('%d %b %Y')
                end_date = (datetime.datetime.now() + timedelta(days=4)).strftime('%d %b %Y')
            subject = "Societies for " + str(all_campaign_name_dict[campaign_id]) + ": " + start_date + " to " + end_date
        elif template_name == 'advanced_booking_details.html':
            if (supplier_list_details_by_status['ongoing_phase']):
                start_date = supplier_list_details_by_status['ongoing_phase']['start_date']
                end_date = supplier_list_details_by_status['ongoing_phase']['end_date']
            else:
                start_date = (datetime.datetime.now() + timedelta(days=1)).strftime('%d %b %Y')
                end_date = (datetime.datetime.now() + timedelta(days=4)).strftime('%d %b %Y')
            subject = str(all_campaign_name_dict[campaign_id]) + " Societies Activation Status for this Weekend (" + start_date + " to " + end_date + ")"
        send_mail_generic.delay(subject, to_array, html, None,None)
    return

def send_mis_contact_report():
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=1)

    all_campaigns = ProposalInfo.objects.filter(tentative_start_date__gte=start_date).all()
    return_list = []
    for campaign in all_campaigns:
        try:
            if "BYJU" in campaign.name:
                partial_dict = {"campaign_name": campaign.name,
                                "total_supplier_count": None,
                                "total_contacts_with_name": 0, 
                                "total_contacts_with_number": 0,
                                }
                all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id).all()
                all_supplier_ids = [ss.object_id for ss in all_shortlisted_spaces]
                all_suppliers = ContactDetails.objects.filter(object_id__in=all_supplier_ids)
                partial_dict["total_supplier_count"] = len(all_shortlisted_spaces)
                for sc in all_suppliers:
                    if sc.mobile:
                        partial_dict["total_contacts_with_number"] += 1
                    if sc.name:
                        partial_dict["total_contacts_with_name"] += 1


                cursor = connection.cursor()
                cursor.execute("SELECT DISTINCT e.society_name, d.proposal_id, r.hashtag, e.Society_City, e.SOCIETY_LOCALITY \
                from shortlisted_inventory_pricing_details as c \
                inner join inventory_activity_assignment as a \
                inner join inventory_activity as b \
                inner join shortlisted_spaces as d \
                inner join supplier_society as e \
                inner join hashtag_images as r \
                on b.id = a.inventory_activity_id and b.shortlisted_inventory_details_id = c.id \
                and c.shortlisted_spaces_id = d.id and d.object_id = e.SUPPLIER_ID and r.object_id = e.supplier_id \
                where d.proposal_id in (%s) and a.activity_date between %s and %s and r.hashtag \
                = 'PERMISSION BOX'", [campaign.proposal_id,start_date, end_date])
                all_list_pb = cursor.fetchall()

                dict_details=['society_name', 'campaign_id', 'hashtag', 'society_city', 'society_locality']
                all_details_list_pb=[dict(zip(dict_details,l)) for l in all_list_pb]

                cursor.execute("SELECT DISTINCT e.society_name, d.proposal_id, r.hashtag, e.Society_City, e.SOCIETY_LOCALITY \
                from shortlisted_inventory_pricing_details as c \
                inner join inventory_activity_assignment as a \
                inner join inventory_activity as b \
                inner join shortlisted_spaces as d \
                inner join supplier_society as e \
                inner join hashtag_images as r \
                on b.id = a.inventory_activity_id and b.shortlisted_inventory_details_id = c.id \
                and c.shortlisted_spaces_id = d.id and d.object_id = e.SUPPLIER_ID and r.object_id = e.supplier_id \
                where d.proposal_id in (%s) and a.activity_date between %s and %s and r.hashtag \
                = 'RECEIPT'", [campaign.proposal_id,start_date, end_date])
                all_list_receipt = cursor.fetchall()
                all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id, is_completed=True).all()
                all_supplier_ids = [ss.object_id for ss in all_shortlisted_spaces]
                dict_details=['society_name', 'campaign_id', 'hashtag', 'society_city', 'society_locality']
                all_details_list_receipt=[dict(zip(dict_details,l)) for l in all_list_receipt]
                partial_dict['count_permission'] = len(all_details_list_pb)
                partial_dict['count_receipt'] = len(all_details_list_receipt)
                partial_dict['supplier_count'] =  len(all_supplier_ids)

                return_list.append(partial_dict)

        except TypeError:
            pass
    template_name = "mis_report_contact.html"
    booking_template = get_template(template_name)

    html = booking_template.render(
        {"partial_dict": return_list})

    subject = "MIS Report"
    to_array = ["shailesh.singh@machadalo.com", "sathya.sharma@machadalo.com", "divya.moses@machadalo.com", 
                "shyamlee.khanna@machadalo.com","srishti.dhamija@machadalo.com", "nikita.walicha@machadalo.com", 
                "prashantgupta888@gmail.com", "kwasi0883@gmail.com", "madhu.atri@machadalo.com", 
                "tejas.pawar@machadalo.com", "jaya.murugan@machadalo.com", "muvaz.khan@machadalo.com",
                "lokesh.kumar@machadalo.com", "vyoma.desai@machadalo.com", "lokesh.kumar@machadalo.com",
                "anupam@machadalo.com", "Anmol.prabhu@machadalo.com", "abhishek.chandel@machadalo.com",
                "momi.borah@machadalo.com"
                ]
    send_mail_generic.delay(subject, to_array, html, None,None)

if ENV == 'prod':
    # schedule.every(10).seconds.do(send_mis_contact_report)
    # schedule.every(1).minutes.do(send_mis_contact_report)
    # schedule.every().hour.do(send_mis_contact_report)
    schedule.every().day.at("23:30").do(send_mis_contact_report) #sends every day at 6pm in IST
    # schedule.every().monday.do(send_mis_contact_report)
    # schedule.every().wednesday.at("13:15").do(send_mis_contact_report)

    while True:
        schedule.run_pending()
        time.sleep(1) 


class SendBookingDetailMails(APIView):
    @staticmethod
    def get(request, campaign_id):
        email_id = request.query_params.get("email", None)
        send_booking_mails_ctrl('booking_details.html', campaign_id, email_id)
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
        # to_array = [user_email] if user_email in campaign_assignement_by_campaign_id[campaign_id] else []
        to_array = ['kshitij.mittal01@gmail.com']
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