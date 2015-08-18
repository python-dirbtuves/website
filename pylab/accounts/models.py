import urllib
import hashlib

import django.contrib.auth.models as auth_models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(auth_models.User, related_name='profile')
    language = models.CharField(_('Language'), max_length=7, choices=settings.LANGUAGES, default='', blank=True)

    def get_avatar_url(self):
        '''Returns avatar associated with email or generated identicon, see more:
        https://secure.gravatar.com/site/implement/images/'''
        if self.user.email:
            user_hash = hashlib.md5(self.user.email.lower().encode('utf-8')).hexdigest()
        else:
            user_hash = hashlib.md5(self.user.username.lower().encode('utf-8')).hexdigest()
        gravatar_url = "http://www.gravatar.com/avatar/%s?" % user_hash
        gravatar_url += urllib.parse.urlencode({'d': 'identicon', 's': '24'})
        return gravatar_url


@receiver(post_save, sender=auth_models.User)
def create_userprofile_for_new_user(sender, instance, **kwargs):  # pylint: disable=unused-argument
    UserProfile.objects.get_or_create(user=instance)
