# Generated by Django 2.1.4 on 2020-09-11 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0054_merge_20200911_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='lead_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='lead_status',
            field=models.CharField(choices=[('very_deep_lead', 'Very Deep Lead'), ('deep_lead', 'Deep Lead'), ('hot_lead', 'Hot Lead'), ('lead', 'Lead'), ('raw_lead', 'Raw Lead')], default='deep_lead', max_length=30),
        ),
    ]
