from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from v0.ui.base.models import BaseModel

class CustomPermissions(BaseModel):
    """
    This is a model which stores extra permissions granted for a particular user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    extra_permission_code = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'custom_permissions'

class ObjectLevelPermission(models.Model):
    """
    This class grants access  Read, Update, View, ViewAll, and UpdateAll on each object it's tied to.
    """
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    view = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    view_all = models.BooleanField(default=False)
    update_all = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'object_level_permission'

class GeneralUserPermission(BaseModel):
    """
    This class defines all the possible functions in website and tells weather that is allowed/not allowed for a profile
    """
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_allowed = models.BooleanField(default=False)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'general_user_permission'


class Role(models.Model):
    """
    This model defines roles
    """
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=255)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'role'

class RoleHierarchy(models.Model):
    """
    This model defines role hierarchy between roles
    """
    parent = models.ForeignKey('Role', related_name='parent', on_delete=models.CASCADE)
    child = models.ForeignKey(Role, on_delete=models.CASCADE)
    depth = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        db_table = 'role_hierarchy'