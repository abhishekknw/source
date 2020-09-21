# Generated by Django 2.1.4 on 2020-09-11 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0049_requirement'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='lead_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.ContactDetails'),
        ),
        migrations.AddField(
            model_name='requirement',
            name='sub_sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.BusinessSubTypes'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.BusinessTypes'),
        ),
        migrations.DeleteModel(
            name='Sector',
        ),
    ]
