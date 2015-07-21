import autoslug
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

import django.contrib.auth.models as auth_models
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(auth_models.User)
    slug = autoslug.AutoSlugField(populate_from='title')
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-details', args=[self.slug])
