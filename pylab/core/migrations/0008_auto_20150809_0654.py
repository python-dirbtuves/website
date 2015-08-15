# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150808_1812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='vote_time',
            new_name='voted',
        ),
    ]
