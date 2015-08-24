# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150809_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='response',
            field=models.PositiveSmallIntegerField(null=True, choices=[(3, 'No'), (2, 'Yes'), (1, 'Maybe')]),
        ),
    ]
