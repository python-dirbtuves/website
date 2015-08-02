# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='responce',
            field=models.PositiveSmallIntegerField(choices=[(2, 'No'), (1, 'Yes'), (0, 'Maybe')], default=0),
        ),
    ]
