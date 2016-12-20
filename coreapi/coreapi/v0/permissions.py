from rest_framework import permissions
import v0.utils as v0_utils



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

