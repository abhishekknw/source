# Generated by Django 2.1.4 on 2020-12-16 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0083_auto_20201214_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='prerequirement',
            name='l1_answer_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='prerequirement',
            name='l2_answer_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='requirement',
            name='l1_answer_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='requirement',
            name='l2_answer_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='prerequirement',
            name='call_back_preference',
            field=models.CharField(choices=[('NA', 'NA'), ('anytime', 'anytime'), ('no need of call. arrange a meeting directly', 'no need of call. arrange a meeting directly'), ('weekday morning', 'weekday morning'), ('weekday evening', 'weekday evening'), ('weekend morning', 'weekend morning'), ('weekend evening', 'weekend evening'), ('customized calling period', 'customized calling period')], default='NA', max_length=100),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='call_back_preference',
            field=models.CharField(choices=[('NA', 'NA'), ('anytime', 'anytime'), ('no need of call. arrange a meeting directly', 'no need of call. arrange a meeting directly'), ('weekday morning', 'weekday morning'), ('weekday evening', 'weekday evening'), ('weekend morning', 'weekend morning'), ('weekend evening', 'weekend evening'), ('customized calling period', 'customized calling period')], default='NA', max_length=100),
        ),
    ]
