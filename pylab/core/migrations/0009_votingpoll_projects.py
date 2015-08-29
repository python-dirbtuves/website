# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150809_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='votingpoll',
            name='projects',
            field=models.ManyToManyField(to='core.Project'),
        ),
    ]
