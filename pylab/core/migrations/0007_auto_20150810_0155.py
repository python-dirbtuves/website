# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150810_0135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_status_description',
            new_name='status_description',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_status',
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Proposed'), (1, 'In progress'), (2, 'Suspended'), (3, 'Implemented')]),
        ),
    ]
