# Generated by Django 2.1.4 on 2020-09-08 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0047_auto_20200907_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'db_table': 'sector',
            },
        ),
    ]
