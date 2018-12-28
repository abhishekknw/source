# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0024_auto_20170109_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('audit_date', models.DateTimeField(default=datetime.datetime(2017, 1, 9, 11, 17, 28, 642959, tzinfo=utc))),
                ('audited_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='closure_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 11, 17, 28, 613759, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='inventory_content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='inventory_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 9, 11, 17, 28, 613723, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='shortlisted_spaces',
            field=models.ForeignKey(blank=True, to='v0.ShortlistedSpaces', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='auditdate',
            name='shortlisted_inventory',
            field=models.ForeignKey(blank=True, to='v0.ShortlistedInventoryPricingDetails', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='audit_dates',
            field=models.ForeignKey(blank=True, to='v0.AuditDate', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
