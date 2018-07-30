from rest_framework import permissions
import v0.utils as v0_utils
from django.core.exceptions import ObjectDoesNotExist
from types import *
from v0.ui.proposal.models import ProposalInfo


class IsOwnerOrManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj=None):

        user = request.user
        # print user.user_profile.all().first().is_cluster_manager
        # print [c.city.city_name for c in user.cities.all()]

        # Read Write permissions are only allowed to the owner or manager of the society .
        if user.user_profile.all().first() and user.user_profile.all().first().is_city_manager:
            return obj.society_city in [item.city.city_name for item in user.cities.all()]

        if user.user_profile.all().first() and user.user_profile.all().first().is_cluster_manager:
            return obj.society_locality in [item.area.label for item in user.clusters.all()]

        return obj.created_by == user or user.is_superuser


class IsMasterUser(permissions.BasePermission):
    """
    checks if the incoming user is a  master user
    """

    def has_permission(self, request, view):
        user = request.user
        return v0_utils.get_group_permission(user, 'master_users')


class IsOpsHead(permissions.BasePermission):
    """
    checks if the incoming user is a ops HEAD
    """

    def has_permission(self, request, view):
        user = request.user
        return v0_utils.get_group_permission(user, 'ops_heads')


class IsBdHead(permissions.BasePermission):
    """
    checks if the incoming user is a BD
    """

    def has_permission(self, request, view):
        user = request.user
        return v0_utils.get_group_permission(user, 'bd_heads')


class IsExternalBd(permissions.BasePermission):
    """
    checks if the incoming user is a external BD
    """

    def has_permission(self, request, view):
        user = request.user
        return v0_utils.get_group_permission(user, 'external_bds')


class IsGeneralBdUser(permissions.BasePermission):
    """
    checks if the incoming user is a general BD user
    """

    def has_permission(self, request, view):
        user = request.user
        return v0_utils.get_group_permission(user, 'general_bd_user')


class IsProposalAuthenticated(permissions.BasePermission):
    """
    takes the proposal_id and user. checks weather the user is authorized to work on this proposal or not
    """

    def has_permission(self, request, view):
        try:
            user = request.user
            # if it's superuser, we return True. The superuser can take any action
            if user.is_superuser:
                return True
            try:
                proposal_id = ''
                keys = ['pk', 'proposal_id']
                if type(request.data) == DictType:
                    proposal_id = request.data.get('proposal_id')
                for key in keys:
                    proposal_id = view.kwargs.get(key)
                    if proposal_id:
                        break
                if not proposal_id:
                    return False
            except KeyError:
                return False
            try:
                # if it's not super user, we check weather the proposal was created by this user only. We only grant
                # CRUD operations on the proposal only if it's been created by the user who is requesting the operations.
                ProposalInfo.objects.get(user=user, proposal_id=proposal_id)
                return True
            except ObjectDoesNotExist:
                return False
        except Exception as e:
            raise Exception("Error in Authenticating this user for the proposal: {0}".format(e.args or e.message))
