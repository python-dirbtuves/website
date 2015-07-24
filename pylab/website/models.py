import autoslug
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    slug = autoslug.AutoSlugField(populate_from='title')
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-details', args=[self.slug])
