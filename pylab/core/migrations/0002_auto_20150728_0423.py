# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_map',
            field=models.URLField(help_text='OpenStreetMap iframe src link.', blank=True, max_length=255),
        ),
    ]
