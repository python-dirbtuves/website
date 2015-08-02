# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150802_0122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='responce',
            new_name='response',
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('attendee', 'event')]),
        ),
    ]
