import django.contrib.auth.models as auth_models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(auth_models.User, related_name='profile')
    language = models.CharField(_('Language'), max_length=7, choices=settings.LANGUAGES, default='', blank=True)
    accepted_terms = models.BooleanField(_('Accept terms of service'), default=False)


@receiver(post_save, sender=auth_models.User)
def create_userprofile_for_new_user(sender, instance, **kwargs):  # pylint: disable=unused-argument
    UserProfile.objects.get_or_create(user=instance)
