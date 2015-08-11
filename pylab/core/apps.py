from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from pylab.core.management import update_default_site


class PylabCoreConfig(AppConfig):
    name = 'pylab.core'
    verbose_name = _("Website")

    def ready(self):
        post_migrate.connect(update_default_site, sender=self)
