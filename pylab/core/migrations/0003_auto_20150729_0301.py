# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150728_0423'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='venue_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='venue_map',
            new_name='osm_map_link',
        ),
    ]
