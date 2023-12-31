# Generated by Django 2.1.4 on 2020-09-11 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0051_requirement_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='preferred_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preferred', to='v0.Organisation'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='v0.Organisation'),
        ),
    ]
