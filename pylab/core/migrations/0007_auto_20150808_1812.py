# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150806_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='points',
            field=models.PositiveIntegerField(verbose_name='Points', null=True, blank=True),
        ),
    ]
