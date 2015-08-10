# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields
import autoslug.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0002_auto_20150728_0303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('starts', models.DateTimeField()),
                ('ends', models.DateTimeField(blank=True, null=True)),
                ('whole_day_event', models.BooleanField(default=False)),
                ('venue_address', models.CharField(max_length=255)),
                ('venue_map', models.CharField(max_length=255, help_text='OpenStreetMap iframe src link.')),
                ('event_type', models.PositiveSmallIntegerField(default=0, choices=[(0, 'Other event'), (1, 'Project development'), (2, 'Initial meeting'), (3, 'Weekly meeting')])),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('parent_event', models.ForeignKey(null=True, blank=True, to='core.Event')),
            ],
        ),
        migrations.SeparateDatabaseAndState(state_operations=[
            migrations.CreateModel(
                name='Project',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                    ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False)),
                    ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, editable=False)),
                    ('slug', autoslug.fields.AutoSlugField(editable=False)),
                    ('title', models.CharField(max_length=255, verbose_name='Title')),
                    ('description', models.TextField(verbose_name='Description')),
                    ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ],
            ),
        ])
    ]
