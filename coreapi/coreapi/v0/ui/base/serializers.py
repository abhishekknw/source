from rest_framework.serializers import ModelSerializer
from v0.managers import check_object_permission
from django.core.exceptions import PermissionDenied
import v0.constants as v0_constants


class BaseModelPermissionSerializer(ModelSerializer):
    """

    Inherit this serializer if you want permission checking in creation of  a model instance through serializer.
    Not sure weather to do this in .save() method or here. Going with serializer.

    """

    def create(self, validated_data):
        """
        called in creating instance. Here we only check fo 'CREATE' permission for the given user.
        :param validated_data:
        :return:
        """
        class_name = self.__class__.__name__
        is_permission, error = check_object_permission(validated_data['user'], self.Meta.model,
                                                       v0_constants.permission_contants['CREATE'])
        if not is_permission:
            raise PermissionDenied(class_name, error)
        return self.Meta.model.objects.create(**validated_data)