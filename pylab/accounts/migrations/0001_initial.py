# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings



def create_userprofiles_for_each_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("accounts", "UserProfile")
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('language', models.CharField(default='', verbose_name='language', max_length=7, choices=[('lt', 'Lithuanian'), ('en', 'English')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_userprofiles_for_each_user),
    ]
