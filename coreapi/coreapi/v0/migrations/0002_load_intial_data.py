# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

# -*- coding: utf-8 -*-

from django.db import models, migrations
from django.core.management import call_command

#fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
#fixture_filename = 'initial_data.json'

fixture = 'initial_data'

def load_data(apps, schema_editor):
    #fixture_file = os.path.join(fixture_dir, fixture_filename)
    call_command('loaddata', fixture, app_label='v0')




class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),

    ]
