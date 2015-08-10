# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150730_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_status',
            field=models.CharField(choices=[('Proposed', 'Proposed'), ('In progress', 'In progress'), ('Suspended', 'Suspended'), ('Implemented', 'Implemented')], max_length=50, default='Proposed'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_status_description',
            field=models.TextField(blank=True, verbose_name='Status Description'),
        ),
        migrations.AddField(
            model_name='project',
            name='url',
            field=models.URLField(blank=True, verbose_name='URL'),
        ),
    ]
