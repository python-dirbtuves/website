# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import django_extensions.db.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('description', models.TextField(verbose_name='Description')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
