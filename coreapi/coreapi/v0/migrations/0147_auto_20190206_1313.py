# Generated by Django 2.1.4 on 2019-02-06 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0146_organisation_created_by_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypebusdepot',
            name='representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.Organisation'),
        ),
        migrations.AddField(
            model_name='suppliertypecorporate',
            name='representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.Organisation'),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.Organisation'),
        ),
        migrations.AddField(
            model_name='suppliertyperetailshop',
            name='representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.Organisation'),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.Organisation'),
        ),
    ]
