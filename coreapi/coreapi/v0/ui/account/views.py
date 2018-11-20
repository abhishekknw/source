import random, string
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.db import transaction
import v0.ui.utils as ui_utils
from models import AccountInfo, BusinessAccountContact, BusinessSubTypes, BusinessTypes
from rest_framework.response import Response
from serializers import BusinessTypesSerializer, AccountInfoSerializer
from v0.ui.supplier.models import SupplierTypeSociety
from v0.ui.organisation.models import Organisation
from v0.ui.account.models import ContactDetails, Signup, ActivityLog
from v0.ui.account.serializers import (BusinessInfoSerializer, BusinessSubTypesSerializer, UIBusinessInfoSerializer,
                                       UIAccountInfoSerializer, BusinessAccountContactSerializer,
                                       ContactDetailsSerializer, SignupSerializer, ActivityLogSerializer)
from v0.ui.common.models import BaseUser
from django.contrib.contenttypes.models import ContentType
import v0.ui.website.utils as website_utils
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from dateutil import tz
from v0.ui.account.models import Profile


class GetBusinessTypesAPIView(APIView):
    """
    fetches all types of businesses.
    """
    def get(self, request, format=None):
        try:
            busTypes = BusinessTypes.objects.all()
            serializer = BusinessTypesSerializer(busTypes, many=True)
            return Response(serializer.data, status=200)
        except :
            return Response(status=404)


class BusinessAPIListView(APIView):
    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request):
        """
        Fetches al businesses belonging to a particular group to which a user belongs.
        Args:
            request: The Request object

        Returns: All businesses.
        """
        class_name = self.__class__.__name__
        try:
            items = Organisation.objects.filter_permission(user=request.user)
            serializer = BusinessInfoSerializer(items, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    #the delete api is not being used
    def delete(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        contacts = item.get_contact_list()
        for contact in contacts:
            contact.delete()
        item.delete()
        return Response(status=204)


class GetBusinessSubTypesAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            items = BusinessSubTypes.objects.filter(business_type_id=id)
            serializer = BusinessSubTypesSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


class BusinessAccounts(APIView):
    """
    Fetches one buissiness data
    """
    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request, id):
        class_name = self.__class__.__name__
        try:
            item = Organisation.objects.get_permission(user=request.user, pk=id)
            business_serializer = UIBusinessInfoSerializer(item)
            accounts = AccountInfo.objects.filter_permission(user=request.user, business=item)
            accounts_serializer = UIAccountInfoSerializer(accounts, many=True)
            response = {
                'business': business_serializer.data,
                'accounts': accounts_serializer.data
            }
            return Response(response, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class Accounts(APIView):

    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request, format=None):
        class_name = self.__class__.__name__
        try:
            items = AccountInfo.objects.filter_permission(user=request.user)
            serializer = AccountInfoSerializer(items, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class AccountAPIView(APIView):

    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request, id, format=None):

        class_name = self.__class__.__name__

        try:
            account = AccountInfo.objects.get_permission(user=request.user, pk=id)
            account_serializer = UIAccountInfoSerializer(account)
            business = Organisation.objects.get(pk=account.organisation_id)
            business_serializer = BusinessInfoSerializer(business)
            '''contacts = AccountContact.objects.filter(account=account)
            serializer3 = AccountContactSerializer(contacts, many=True)'''

            data = {'account': account_serializer.data, 'business': business_serializer.data}
            return Response(data, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class BusinessContacts(APIView):

    # permission_classes = (v0_permissions.IsGeneralBdUser,)

    def post(self, request):
        class_name = self.__class__.__name__
        """

        ---
        parameters:
        - name: business
          description: a dict having keys buisiness_id, business_type_id, sub_type_id, name, contacts.
          paramType: body

        """

        current_user = request.user

        business_data = request.data.get('business')
        if not business_data:
            return Response(data={'status': False, 'error': 'No business data supplied'},
                            status=status.HTTP_400_BAD_REQUEST)

        business_data['type_name'] = business_data['business_type_id']
        business_data['sub_type'] = business_data['sub_type_id']

        type_name = BusinessTypes.objects.get(id=int(business_data['business_type_id']))
        sub_type = BusinessSubTypes.objects.get(id=int(business_data['sub_type_id']))

        business_data['user'] = current_user.id
        try:
            with transaction.atomic():

                business_serializer_data = {}

                if 'organisation_id' in business_data:
                    business = Organisation.objects.get_permission(user=request.user,
                                                                   pk=business_data['organisation_id'])
                    serializer = BusinessInfoSerializer(business, data=business_data)
                else:
                    business_data['organisation_id'] = self.generate_organisation_id(
                        business_name=business_data['name'], sub_type=sub_type, type_name=type_name)
                    if business_data['organisation_id'] is None:
                        # if organisation_id is None --> after 12 attempts couldn't get unique id so return first id in lowercase
                        business_data['organisation_id'] = self.generate_organisation_id(business_data['name'],
                                                                                         sub_type=sub_type,
                                                                                         type_name=type_name,
                                                                                         lower=True)
                    serializer = BusinessInfoSerializer(data=business_data)

                if serializer.is_valid():
                    serializer.save()
                    business_serializer_data = serializer.data
                    business_serializer_data['business_sub_type'] = sub_type.business_sub_type
                    business_serializer_data['business_type'] = type_name.business_type

                business = Organisation.objects.get_permission(user=current_user, pk=business_data['organisation_id'])
                content_type_business = ContentType.objects.get_for_model(Organisation)
                contact_ids = list(business.contacts.all().values_list('id', flat=True))
                contact_list = []

                for contact in business_data['contacts']:

                    contact['object_id'] = business.organisation_id
                    contact['content_type'] = content_type_business.id
                    contact['user'] = current_user.id

                    if 'id' in contact:
                        item = BusinessAccountContact.objects.get(pk=contact['id'])
                        if contact['spoc'] == '':
                            contact['spoc'] = item.spoc
                        contact_ids.remove(item.id)
                        contact_serializer = BusinessAccountContactSerializer(item, data=contact)
                    else:
                        if contact['spoc'] == '':
                            contact['spoc'] = 'false'
                        contact_serializer = BusinessAccountContactSerializer(data=contact)

                    if contact_serializer.is_valid():
                        contact = contact_serializer.save()
                        contact_list.append(contact)
                    else:
                        return ui_utils.handle_response(class_name, data=contact_serializer.errors)

                # deleting all contacts whose id not received from the frontend
                BusinessAccountContact.objects.filter(id__in=contact_ids).delete()

                contacts_serializer = BusinessAccountContactSerializer(contact_list, many=True)
                business_serializer = UIBusinessInfoSerializer(business)

                response = {
                    'business': business_serializer.data,
                    'contacts': contacts_serializer.data,
                }
                return Response(response, status=200)
        except Exception as e:
                return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def generate_organisation_id(self, business_name, sub_type, type_name, lower=False):
        business_code = create_code(name=business_name)
        business_front = type_name.business_type_code + sub_type.business_sub_type_code
        organisation_id = business_front + business_code
        if lower:
            return organisation_id.lower()

        try:
            business = Organisation.objects.get(organisation_id=organisation_id)
            # if exception does not occur means conflict
            business_code = create_code(name=business_name, conflict=True)
            organisation_id = type_name.business_type_code + sub_type.business_sub_type_code + business_code
            business = Organisation.objects.get(organisation_id=organisation_id)

            # still conflict ---> Generate random 4 uppercase character string
            i = 0  # i keeps track of infinite loop tune it according to the needs
            while (True):
                if i > 10:
                    return None
                business_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
                organisation_id = business_front + business_code
                business = Organisation.objects.get(organisation_id=organisation_id)
                i += 1

        except Organisation.DoesNotExist:
            return organisation_id.upper()


def create_code(name, conflict=False):
    name = name.split()

    if len(name) >= 4:
        code = name[0][0] + name[1][0] + name[2][0] + name[3][0]
    if len(name) == 3:
        if len(name[0]) >= 2:
            code = name[0][:2] + name[1][0] + name[2][0]
        else :
            code = get_extra_character() + name[0] + name[1][0] + name[2][0]
    elif len(name) == 2:
        if len(name[0]) >= 2 and len(name[1]) >= 2:
            code = name[0][:2] + name[1][:2]
        elif len(name[0]) >= 3:
            code = name[0][:3] + name[1]
        elif len(name[1]) >= 3:
            code = name[0] + name[1][:3]
        elif len(name[0]) >= 2 or len(name[0]) >=2:
            code = get_extra_character() + name[0] + name[1]
        else :
            code = get_extra_character(size=2) + name[0] + name[1]
    else:
        if len(name[0]) >= 4:
            code = name[0][:4]
        else :
            size = 4 - len(name[0])
            extra_characters = get_extra_character(size)
            code = extra_characters + name[0]

    # conflict means previous code already present in database
    # so append a extra char in front of existing code and remove last char from it
    if conflict:
        code = get_extra_character() + code[:3]
    return code.upper()


def get_extra_character(size=1):
    return ''.join(random.choice(string.ascii_uppercase ) for _ in range(size))


class AccountContacts(APIView):
    """
    API creates Account for a business
    """
    def post(self, request):
        class_name = self.__class__.__name__
        try:
            response = {}
            current_user = request.user

            account_data = request.data['account']

            with transaction.atomic():

                organisation_id = account_data['organisation_id']
                # checking a valid business

                business = Organisation.objects.get(pk=organisation_id)

                if 'account_id' in account_data:
                    account = AccountInfo.objects.get(pk=account_data['account_id'])
                    serializer = AccountInfoSerializer(account, data=account_data)
                else:
                    account_data['account_id']= self.generate_account_id(account_name=account_data['name'],organisation_id=organisation_id)
                    if account_data['account_id'] is None:
                        # if account_id is None --> after 12 attempts couldn't get unique id so return first id in lowercase
                        account_data['account_id'] = self.generate_account_id(account_name=account_data['name'],organisation_id=organisation_id, lower=True)
                    serializer = AccountInfoSerializer(data=account_data)

                if serializer.is_valid():
                    account = serializer.save(business=business, user=current_user)
                else:
                    return Response(serializer.errors, status=400)

                content_type_account = ContentType.objects.get_for_model(AccountInfo)

                # #here we will start storing contacts
                contact_ids = list(account.contacts.all().values_list('id',flat=True))
                contact_list = []

                for contact in account_data['contacts']:
                    contact['object_id'] = account.account_id
                    contact['content_type'] = content_type_account.id
                    contact['user'] = current_user.id

                    if 'id' in contact:
                        item = BusinessAccountContact.objects.get(pk=contact['id'])
                        contact_ids.remove(item.id)
                        if contact['spoc'] == '':
                            contact['spoc'] = item.spoc
                        contact_serializer = BusinessAccountContactSerializer(item, data=contact)
                    else:
                        if contact['spoc'] == '':
                            contact['spoc'] = 'false'
                        contact_serializer = BusinessAccountContactSerializer(data=contact)

                    if contact_serializer.is_valid():
                        contact = contact_serializer.save()
                        contact_list.append(contact)
                    else:
                        return Response(contact_serializer.errors, status=400)

                BusinessAccountContact.objects.filter(id__in=contact_ids).delete()
                account_serializer = AccountInfoSerializer(account)
                contacts_serializer = BusinessAccountContactSerializer(contact_list, many=True)
                response['account'] = account_serializer.data
                response['contacts'] = contacts_serializer.data
            return Response(response, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def generate_account_id(self, account_name, organisation_id, lower=False):
        business_code = organisation_id[-4:]
        account_code = create_code(name = account_name)
        account_id = business_code + account_code

        try:
            account = AccountInfo.objects.get(account_id=account_id)
            # if exception does not occur means confict
            account_code = create_code(name = account_name, conflict=True)
            account_id = business_code + account_code
            account = AccountInfo.objects.get(account_id=account_id)

            # still conflict ---> Generate random 4 uppercase character string
            i = 0  # i keeps track of infinite loop tune it according to the needs
            while True:
                if i > 10:
                    return None
                account_code = ''.join(random.choice(string.ascii_uppercase ) for _ in range(4))
                account_id = business_code + account_code
                account = AccountInfo.objects.get(account_id=account_id)
                i += 1

        except AccountInfo.DoesNotExist:
            return account_id.upper()


class AccountViewSet(viewsets.ViewSet):
    """
    viewset that around AcountInfo model
    """
    def list(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            organisation_id = request.query_params['organisation_id']
            accounts = AccountInfo.objects.filter_permission(user=request.user, organisation=Organisation.objects.get(pk=organisation_id))
            serializer = AccountInfoSerializer(accounts, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk):
        """

        :param request:
        :param pk:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            account = AccountInfo.objects.get_permission(user=request.user, pk=pk)
            account_serializer = AccountInfoSerializer(account)
            contacts = ContactDetails.objects.filter(object_id=pk)
            contact_serializer = ContactDetailsSerializer(contacts, many=True)
            data = {
                'account' : account_serializer.data,
                'contacts' : contact_serializer.data
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def create(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            data = request.data.copy()
            data['user'] = request.user.pk
            organisation_name = Organisation.objects.get(pk=data['organisation']).name
            data['account_id'] = website_utils.get_generic_id([organisation_name, data['name']])
            serializer = AccountInfoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = website_utils.create_contact_details(data['account_id'],data['contacts'])
                if not response.data['status']:
                    return response
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk):
        """

        :param request:
        :param pk:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            data = request.data.copy()
            account = AccountInfo.objects.get_permission(user=request.user, check_update_permissions=True, pk=pk)
            serializer = AccountInfoSerializer(data=data, instance=account)
            if serializer.is_valid():
                serializer.save()
                response = website_utils.update_contact_details(pk, data['contacts'])
                if not response.data['status']:
                    return response
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class SignupAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Signup.objects.get(pk=id)
            serializer = SignupSerializer(item)
            return Response(serializer.data)
        except Signup.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Signup.objects.get(pk=id)
        except Signup.DoesNotExist:
            return Response(status=404)
        serializer = SignupSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Signup.objects.get(pk=id)
        except Signup.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class SignupAPIListView(APIView):

    def get(self, request, format=None):
        items = Signup.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SignupSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    user_id = user.id
    profile_id = user.profile_id
    profile = Profile.objects.filter(id=profile_id).all()
    if len(profile) == 0:
        return
    organisation_id = profile[0].organisation_id
    serializer = ActivityLogSerializer(data={"user": user_id, "organisation": organisation_id})
    if serializer.is_valid():
        serializer.save()
    return


class LoginLog(APIView):
    def get(self, request):
        page_no = int(request.GET.get('page', 1))
        total_logs = 25
        user = request.user
        user_id = user.id
        profile_id = user.profile_id
        profile = Profile.objects.filter(id=profile_id).all()
        if len(profile) == 0:
            return
        organisation_id = profile[0].organisation_id
        organisation = Organisation.objects.get(organisation_id=organisation_id)
        activity_log = ActivityLog.objects.filter(organisation_id=organisation_id).order_by('-created_at')[total_logs * (page_no-1):total_logs * (page_no)].all()
        log_data = []
        for activity in activity_log:
            curr_activity = {}
            curr_activity['organisation_name'] = organisation.name
            curr_activity['organisation_id'] = organisation.organisation_id
            curr_activity['user_id'] = activity.user.id
            curr_activity['username'] = activity.user.username
            curr_activity['first_name'] = activity.user.first_name
            curr_activity['last_name'] = activity.user.last_name
            curr_activity['email'] = activity.user.email
            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz('Asia/Kolkata')
            curr_activity['login_timestamp'] = activity.created_at.replace(tzinfo=from_zone).astimezone(to_zone)
            log_data.append(curr_activity)
        return ui_utils.handle_response({}, data=log_data, success=True)
