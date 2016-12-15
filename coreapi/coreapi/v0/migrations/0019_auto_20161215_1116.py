# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0018_auto_20161215_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='adinventorytype',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='adinventorytype',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='durationtype',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='durationtype',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='flattype',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='flattype',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='flyerinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='flyerinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='imagemapping',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='imagemapping',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='noticeboarddetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='noticeboarddetails',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='poleinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='poleinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='posterinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='posterinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='societymajorevents',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='societymajorevents',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='standeeinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='standeeinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='wallinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='wallinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
    ]
