from rest_framework import viewsets
from serializers import (ObjectLevelPermissionSerializer, GeneralUserPermissionSerializer, RoleSerializer)
from models import ObjectLevelPermission, GeneralUserPermission, Role, RoleHierarchy
import v0.ui.utils as ui_utils
import v0.ui.website.utils as website_utils
from rest_framework.response import Response
from v0.ui.organisation.models import Organisation
from v0.ui.common.models import BaseUser
from v0.ui.account.models import Profile, AccountInfo
from v0.ui.proposal.models import ProposalInfo
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from datetime import datetime


class GeneralUserPermissionViewSet(viewsets.ViewSet):
    """
    ViewSet around general user permission model
    """

    def list(self, request):
        """
        retrieves all general user permission in the system
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            instances = GeneralUserPermission.objects.all()
            serializer = GeneralUserPermissionSerializer(instances, many=True)
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
            instance = GeneralUserPermission.objects.get(pk=pk)
            serializer = GeneralUserPermissionSerializer(instance)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
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
            data['codename'] = "".join(data['name'].split()[:2]).upper()
            data['name'] = "_".join(data['name'].split(" "))
            serializer = GeneralUserPermissionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
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
            instance = GeneralUserPermission.objects.get(pk=pk)
            serializer = GeneralUserPermissionSerializer(data=request.data, instance=instance)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class ObjectLevelPermissionViewSet(viewsets.ViewSet):
    """
    ViewSet around object level permission model
    """
    def list(self, request):
        """
        retrieves all Object level permission in the system
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            # change this list if you want more models
            valid_models = [Organisation, BaseUser, Profile, AccountInfo, ProposalInfo]
            instances = ObjectLevelPermission.objects.filter(content_type__in= ContentType.objects.get_for_models(*valid_models).values())
            serializer = ObjectLevelPermissionSerializer(instances, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk):
        """
        :return:
        """
        class_name = self.__class__.__name__
        try:
            instance = ObjectLevelPermission.objects.get(pk=pk)
            serializer = ObjectLevelPermissionSerializer(instance)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
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
            data['codename'] = ''.join(data['name'].split(' '))
            serializer = ObjectLevelPermissionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
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
            instance = ObjectLevelPermission.objects.get(pk=pk)
            serializer = ObjectLevelPermissionSerializer(data=request.data, instance=instance)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class RoleViewSet(viewsets.ViewSet):
    """
    viewset around roles
    """
    def create(self,request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            data = request.data.copy()
            data['codename'] = "".join(data['name'].split()[:2]).upper()
            serializer = RoleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                website_utils.create_entry_in_role_hierarchy(serializer.data)
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def list(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            organisation_id = request.query_params['organisation_id']
            roles = Role.objects.filter(organisation=Organisation.objects.get(pk=organisation_id))
            serializer = RoleSerializer(roles, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class RoleHierarchyViewSet(viewsets.ViewSet):
    """
    viewset arounnd Role hierarchy, deletes previous hierarchy and create new one
    """
    def create(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            data = request.data.copy()
            child_instance = Role.objects.get(pk=data['child'])
            old_role_hierarchy_objects = RoleHierarchy.objects.filter(child=data['child'])
            old_role_hierarchy_objects.delete()
            new_role_hierachy_objects = RoleHierarchy.objects.filter(child=data['parent'])
            role_objects = []
            for instance in new_role_hierachy_objects:
                role_data = {
                    'parent' : instance.parent,
                    'child' : child_instance,
                    'depth' : instance.depth + 1
                }
                role_objects.append(RoleHierarchy(**role_data))
            role_data = {
            'parent' : child_instance,
            'child'  : child_instance,
            }
            role_objects.append(RoleHierarchy(**role_data))
            RoleHierarchy.objects.bulk_create(role_objects)
            return Response(status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class ManualGeneralUserPermissions(APIView):

    def post(self, request):
        class_name = self.__class__.__name__
        permissions_list = request.data
        all_profile_ids = Profile.objects.values_list('id', flat=True)
        all_permission_object_list = []
        for profile_id in all_profile_ids:
            for permission in permissions_list:
                all_permission_object_list.append(GeneralUserPermission(**{
                    'name': permission,
                    'is_allowed': False,
                    'profile_id': profile_id,
                    'codename': "".join(permission.split("_")[:2]).upper(),
                    'created_at': datetime.now()
                }))
        GeneralUserPermission.objects.bulk_create(all_permission_object_list)
        return ui_utils.handle_response(class_name, data='success', success=True)

