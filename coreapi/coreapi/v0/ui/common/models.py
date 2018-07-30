from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from v0.ui.permissions.models import Role


class BaseUser(AbstractUser):
    """
    This is base user class that inherits AbstractBaseUser and adds an additional field.
    """
    user_code = models.CharField(max_length=255, default=settings.DEFAULT_USER_CODE)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    profile = models.ForeignKey('Profile', null=True, blank=True)  # remove null=true once every user has been attached one profile
    role = models.ForeignKey(Role, null=True, blank=True)

    class Meta:
        db_table = 'base_user'