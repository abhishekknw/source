# Generated by Django 2.1.4 on 2020-06-30 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0035_auto_20200630_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalinfo',
            name='type_of_end_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.TypeOfEndCustomer'),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='bk_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.BookingStatus'),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='bk_substatus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.BookingSubstatus'),
        ),
    ]
