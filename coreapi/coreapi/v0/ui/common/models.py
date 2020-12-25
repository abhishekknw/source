from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from v0.ui.permissions.models import Role
from pymongo import MongoClient
# client = MongoClient('localhost', settings.MONGO_PORT, username=settings.MONGO_USER, password=settings.MONGO_PASSWORD, maxPoolSize=2, waitQueueMultiple=10)
# mongo_client = client[settings.MONGO_DB]
client = MongoClient(settings.MONGO_CONNECTION)
mongo_client = client.get_default_database()
mongo_test = client[settings.MONGO_DB_TEST]


class BaseUser(AbstractUser):
    """
    This is base user class that inherits AbstractBaseUser and adds an additional field.
    """
    user_code = models.CharField(max_length=255, default=settings.DEFAULT_USER_CODE)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    profile = models.ForeignKey('Profile', null=True, blank=True, on_delete=models.CASCADE)  # remove null=true once every user has been attached one profile
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.CASCADE)
    terms_accepted = models.BooleanField(default=False)
    emailVerifyCode = models.CharField(max_length=20, null=True, blank=True)
    emailVerifyDate = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'base_user'

    def save(self, *args, **kwargs):
        mongo_client.api_cache.remove({"slugType": 'user-list'})
        super(BaseUser, self).save(*args, **kwargs)