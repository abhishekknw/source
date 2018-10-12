from rest_framework.views import APIView
from coreapi.settings import BASE_URL, BASE_DIR
import v0.constants as v0_constants
import v0.ui.website.utils as website_utils
import v0.ui.utils as ui_utils
from smtplib import SMTPException
from celery import shared_task
from django.core.mail import EmailMessage
from models import EmailSettings
from v0.ui.leads.views import get_leads_excel_sheet
from v0.ui.leads.models import LeadsForm
from v0.ui.campaign.models import CampaignAssignment
from v0.ui.proposal.models import ProposalInfo
import datetime
import os
import magic

@shared_task()
def send_email(email_data, attachment=None):
    """
    Args: dict having 'subject', 'body' and 'to' as keys.
    Returns: success if mail is sent else failure
    """
    function = send_email.__name__
    try:
        email_keys = email_data.keys()
        for key in v0_constants.valid_email_keys:
            if key not in email_keys:
                raise Exception(function, 'key {0} not found in the recieved structure'.format(key))
        email = EmailMessage(email_data['subject'], email_data['body'], to=email_data['to'])
        if attachment:
            filepath = attachment['filepath']
            file_to_send = open(filepath, 'r')
            filename = filepath[filepath.rfind('/')+1:]
            email.attach(filename, file_to_send.read(), attachment['mime_type'])
            file_to_send.close()
        email_send_return = email.send()
        os.unlink(filepath)
        return email_send_return
    except SMTPException as e:
        raise Exception(function, "Error " + ui_utils.get_system_error(e))
    except Exception as e:
        raise Exception(function, "Error " + ui_utils.get_system_error(e))


def send_mail_with_attachment(filepath, subject, to):
    filepath = filepath if filepath else BASE_DIR + '/files/sample_mail_file.xlsx'
    filename = filepath[filepath.rfind('/')+1:]
    with open(filepath, 'rb') as content_file:
        my_file = content_file.read()
    template_body = v0_constants.email['body']
    body_mapping = {
        'file': filename
    }
    modified_body = website_utils.process_template(template_body, body_mapping)
    email_data = {
        'subject': subject,
        'to': to,
        'body': modified_body
    }
    attachment = None
    mime = magic.Magic(mime=True)
    if my_file:
        attachment = {
            'filepath': filepath,
            'mime_type': mime.from_file(filepath)
        }
    task_id = send_email.delay(email_data, attachment).id
    return task_id


class SendMail(APIView):
    """
    API sends mail. The API sends a file called 'sample_mail_file.xlsx' located in files directory.
    API  is for testing purpose only.

    """
    def post(self, request):
        class_name = self.__class__.__name__
        try:
            subject = str(request.data['subject'])
            to = [str(request.data['to'])]
            task_id = send_mail_with_attachment(None, subject, to)
            return ui_utils.handle_response(class_name, data={'task_id': task_id}, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class Mail(APIView):
    """
    API sends mail. The API sends a simple mail to a single person
    """
    def post(self, request):
        class_name = self.__class__.__name__
        try:
            # takes these params from request
            subject = request.data['subject']
            to = request.data['to']
            body = request.data['body']

            email_data = {
                'subject': subject,
                'to': [to, ],
                'body': body
            }
            attachment = None
            task_id = send_email.delay(email_data, attachment).id
            return ui_utils.handle_response(class_name, data={'task_id': task_id}, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


def send_weekly_leads_email():
    all_leads_forms = LeadsForm.objects.values('id', 'campaign_id').all()
    all_campaign_id_list = [leads_form['campaign_id'] for leads_form in all_leads_forms]
    all_campaign_assignment = CampaignAssignment.objects.filter(campaign_id__in=all_campaign_id_list).values('campaign_id', 'assigned_to__email').all()
    campaign_assignement_by_campaign_id = {}
    all_campaign_name = ProposalInfo.objects.filter(proposal_id__in=all_campaign_id_list).values('proposal_id', 'name')
    all_campaign_name_dict = {campaign['proposal_id']: campaign['name'] for campaign in all_campaign_name}
    for campaign_assignement in all_campaign_assignment:
        if campaign_assignement['campaign_id'] not in campaign_assignement_by_campaign_id:
            campaign_assignement_by_campaign_id[campaign_assignement['campaign_id']] = []
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
            # send_mail_with_attachment(filepath, "Weekly Leads Data", to_array)
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


class EmailSettingsView(APIView):
    @staticmethod
    def post(request):
        user_id = request.data['user_id']
        email_types = request.data['email_types']  # list of dict with name and is_allowed keys
        list_of_objects = []
        for email_type in email_types:
            list_of_objects.append(EmailSettings(**{
                "user_id": user_id,
                "email_type": email_type["name"],
                "is_allowed": email_type["is_allowed"],
            }))
        EmailSettings.objects.bulk_create(list_of_objects)
        return ui_utils.handle_response('', data={"success": True}, success=True)

