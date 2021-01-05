# Generated by Django 2.1.4 on 2020-06-01 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20200525_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierrelationship',
            name='type',
            field=models.CharField(default='PREFERRED', max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='supplierrelationship',
            unique_together={('society', 'supplier_id', 'type')},
        ),
    ]