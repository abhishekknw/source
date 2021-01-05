# Generated by Django 2.1.4 on 2020-05-09 16:01

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0030_billinginventory_busbackinventory_busleftinventory_busrightinventory_busshelterinventory_busshelterl'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosterLiftInventory',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('adinventory_id', models.CharField(db_column='ADINVENTORY_ID', max_length=22, unique=True)),
                ('object_id', models.CharField(max_length=20, null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'poster_lift_inventory',
            },
        ),
    ]