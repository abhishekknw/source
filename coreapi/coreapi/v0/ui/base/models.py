from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    """
    This is base model to be inherited by any model which uses time stamps.
    Because at the time of creation of this model, the data already exists in the db so we need some kind
    of default value to populate existing rows. A default date of 2016-12-1 is defined in settings.py which
    is used to populate existing rows. So when object of model is created for the first time, created_at
    field is checked for the default value defined in settings. If it's same, we update the created_at field.

    """
    created_at = models.DateTimeField(editable=False, default=settings.DEFAULT_DATE)
    updated_at = models.DateTimeField(editable=False, default=settings.DEFAULT_DATE)

    def save(self, *args, **kwargs):
        # save the current time
        current_time = timezone.now()

        if self.pk is None:
            # if pk is None, object is new in general. set created_at updated_at to the same time.
            self.created_at = self.updated_at = current_time
        else:
            # if pk is Not None, then object may be an old one or in some cases new one
            # it is a new object if we use UUID as pk field or we pass pk in .create() method
            # and  pk is not None in that case.
            try:
                # pk is Not none, it can be an old instance or a new instance in some cases.
                # if object is found, then it is indeed an old instance.
                self.__class__.objects.get(pk=self.pk)
                self.updated_at = current_time
                # in some case if self.created_at is not already set, set it here
                if not self.created_at:
                    self.created_at = current_time

            except ObjectDoesNotExist:
                # if pk does not exist, this is  a new instance
                self.created_at = self.updated_at = current_time

        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True