# Generated by Django 2.1.4 on 2020-10-27 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0071_auto_20201021_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='company_campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.ProposalInfo'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='company_shortlisted_spaces',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.ShortlistedSpaces'),
        ),
    ]