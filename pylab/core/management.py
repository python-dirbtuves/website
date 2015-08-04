from django.apps import apps
from django.conf import settings


def update_default_site(app_config, verbosity=2, **kwargs):
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get_current()

    if site.domain == 'example.com':
        site.domain = settings.SERVER_NAME
        site.name = 'pylab.lt'
        site.save()
