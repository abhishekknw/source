from rest_framework import permissions


class IsOwnerOrManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj=None):

        user = request.user
        #print user.user_profile.all().first().is_cluster_manager
        #print [c.city.city_name for c in user.cities.all()]

        # Read Write permissions are only allowed to the owner or manager of the society .
        if user.user_profile.all().first().is_city_manager:
            return obj.society_city in [item.city.city_name for item in user.cities.all()]

        if user.user_profile.all().first().is_cluster_manager:
            return obj.society_locality in [item.area.label for item in user.clusters.all()]

        return obj.created_by == user or user.is_superuser
