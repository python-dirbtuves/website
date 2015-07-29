# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150729_0301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='whole_day_event',
            new_name='hide_time',
        ),
    ]
