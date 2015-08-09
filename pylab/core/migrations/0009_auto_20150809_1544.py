# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150802_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(blank=True, editable=False, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='attendance',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(blank=True, editable=False, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='response',
            field=models.PositiveSmallIntegerField(null=True, choices=[(2, 'No'), (1, 'Yes'), (0, 'Maybe')]),
        ),
    ]
