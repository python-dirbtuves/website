# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_comments', '0002_update_user_email_field_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentComment',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_comments.Comment')),
                ('parent_comment', models.ForeignKey(to='custom_comment_app.ParentComment', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('django_comments.comment',),
        ),
    ]
