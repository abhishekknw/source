# Generated by Django 2.1.4 on 2020-09-08 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0048_sector'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impl_timeline', models.CharField(choices=[('immediate', 'immediate'), ('next 2-4 months', 'next 2-4 months'), ('after 4 months', 'after 4 months'), ("don't know", "don't know")], default='next 2-4 months', max_length=30)),
                ('meating_timeline', models.CharField(choices=[('immediate', 'immediate'), ('next 15 days-2 months', 'next 15 days-2 months'), ('after 2 months', 'after 2 months'), ("don't know", "don't know")], default='next 15 days-2 months', max_length=30)),
                ('lead_status', models.CharField(choices=[('very_deep_lead', 'very_deep_lead'), ('deep_lead', 'deep_lead'), ('hot_lead', 'hot_lead'), ('lead', 'lead'), ('raw_lead', 'raw_lead')], default='deep_lead', max_length=30)),
                ('comment', models.TextField(blank=True, max_length=500)),
                ('varified', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preferred', to='v0.Organisation')),
                ('current_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current', to='v0.Organisation')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.Sector')),
                ('shortlisted_spaces', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.ShortlistedSpaces')),
            ],
            options={
                'db_table': 'requirement',
            },
        ),
    ]