# Generated by Django 2.1.4 on 2020-11-06 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0074_requirement_varified_bd_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='lead_price',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='lead_status',
            field=models.CharField(choices=[('Very Deep Lead', 'Very Deep Lead'), ('Deep Lead', 'Deep Lead'), ('Hot Lead', 'Hot Lead'), ('Lead', 'Lead'), ('Raw Lead', 'Raw Lead'), ('Warm Lead', 'Warm Lead')], default='Deep Lead', max_length=30),
        ),
    ]
