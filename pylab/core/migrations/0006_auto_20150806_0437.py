# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields
import django.utils.timezone
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20150730_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('vote_time', models.DateTimeField(null=True)),
                ('points', models.IntegerField(verbose_name='Points', null=True)),
                ('project', models.ForeignKey(to='core.Project')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VotingPoll',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='vote',
            name='voting_poll',
            field=models.ForeignKey(to='core.VotingPoll'),
        ),
    ]
