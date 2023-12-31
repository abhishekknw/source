# Generated by Django 2.1.4 on 2020-12-10 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0081_auto_20201207_0450'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_company_other', models.CharField(blank=True, max_length=50, null=True)),
                ('preferred_company_other', models.CharField(blank=True, max_length=50, null=True)),
                ('impl_timeline', models.CharField(choices=[('within 2 weeks', 'within 2 weeks'), ('within 2 months', 'within 2 months'), ('2 months to 6 months', '2 months to 6 months'), ('6 months to 1 year', '6 months to 1 year'), ('1 year to 1.5 years', '1 year to 1.5 years'), ('<1month', '<1month'), ('1-3 months', '1-3 months'), ('4-6 months', '4-6 months'), ('>6 months', '>6 months'), ('yet not decided', 'yet not decided'), ('not given', 'not given')], default='within 2 months', max_length=30)),
                ('meating_timeline', models.CharField(choices=[('as soon as possible', 'as soon as possible'), ('within 1 week', 'within 1 week'), ('within a month', 'within a month'), ('after a month', 'after a month'), ('not given', 'not given')], default='within 1 week', max_length=30)),
                ('lead_status', models.CharField(choices=[('Very Deep Lead', 'Very Deep Lead'), ('Deep Lead', 'Deep Lead'), ('Hot Lead', 'Hot Lead'), ('Lead', 'Lead'), ('Raw Lead', 'Raw Lead'), ('Warm Lead', 'Warm Lead')], default='Deep Lead', max_length=30)),
                ('comment', models.TextField(blank=True, max_length=500, null=True)),
                ('is_current_patner', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5)),
                ('current_patner_feedback', models.CharField(choices=[('NA', 'NA'), ('Satisfied', 'Satisfied'), ('Dissatisfied', 'Dissatisfied'), ('Extremely Dissatisfied', 'Extremely Dissatisfied')], default='NA', max_length=50)),
                ('current_patner_feedback_reason', models.CharField(blank=True, max_length=250, null=True)),
                ('varified_ops', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5)),
                ('varified_ops_date', models.DateTimeField(null=True)),
                ('varified_bd', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5)),
                ('varified_bd_date', models.DateTimeField(null=True)),
                ('is_deleted', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5)),
                ('lead_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('l1_answers', models.CharField(blank=True, max_length=100, null=True)),
                ('l2_answers', models.CharField(blank=True, max_length=100, null=True)),
                ('change_current_patner', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5)),
                ('lead_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('call_back_preference', models.CharField(blank=True, max_length=100, null=True)),
                ('lead_purchased', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5)),
                ('purchased_date', models.DateTimeField(null=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='campaign', to='v0.ProposalInfo')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_company', to='v0.Organisation')),
                ('company_campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_company_campaign', to='v0.ProposalInfo')),
                ('company_shortlisted_spaces', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_company_shortlisted_spaces', to='v0.ShortlistedSpaces')),
                ('current_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_current', to='v0.Organisation')),
                ('lead_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='v0.ContactDetails')),
                ('preferred_company', models.ManyToManyField(blank=True, null=True, related_name='pre_preferred', to='v0.Organisation')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sector', to='v0.BusinessTypes')),
                ('shortlisted_spaces', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shortlisted', to='v0.ShortlistedSpaces')),
                ('sub_sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_Sector', to='v0.BusinessSubTypes')),
                ('varified_bd_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_varified_bd_by', to=settings.AUTH_USER_MODEL)),
                ('varified_ops_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pre_varified_ops_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pre_requirement',
            },
        ),
        migrations.AlterField(
            model_name='requirement',
            name='impl_timeline',
            field=models.CharField(choices=[('within 2 weeks', 'within 2 weeks'), ('within 2 months', 'within 2 months'), ('2 months to 6 months', '2 months to 6 months'), ('6 months to 1 year', '6 months to 1 year'), ('1 year to 1.5 years', '1 year to 1.5 years'), ('<1month', '<1month'), ('1-3 months', '1-3 months'), ('4-6 months', '4-6 months'), ('>6 months', '>6 months'), ('yet not decided', 'yet not decided'), ('not given', 'not given')], default='within 2 months', max_length=30),
        ),
    ]
