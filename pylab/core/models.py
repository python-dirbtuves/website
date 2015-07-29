from autoslug import AutoSlugField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User)
    slug = AutoSlugField(populate_from='title')
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-details', args=[self.slug])


class Event(models.Model):
    OTHER = 0
    PROJECT_DEVELOPMENT = 1
    INITIAL_MEETING = 2
    WEEKLY_MEETING = 3
    EVENT_TYPE_CHOICES = (
        (OTHER, _("Other event")),
        (PROJECT_DEVELOPMENT, _("Project development")),
        (INITIAL_MEETING, _("Initial meeting")),
        (WEEKLY_MEETING, _("Weekly meeting")),
    )

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User)
    slug = AutoSlugField(populate_from='title')
    parent_event = models.ForeignKey('self', null=True, blank=True)
    event_type = models.PositiveSmallIntegerField(choices=EVENT_TYPE_CHOICES, default=OTHER)
    title = models.CharField(_("Title"), max_length=255)
    starts = models.DateTimeField()
    ends = models.DateTimeField(null=True, blank=True)
    hide_time = models.BooleanField(default=False)  # If True, do not show time in starts and ends dates.
    description = models.TextField(_("Description"), blank=True)
    address = models.CharField(max_length=255, blank=True)
    osm_map_link = models.URLField(max_length=255, blank=True, help_text=_("OpenStreetMap iframe src link."))

    def __str__(self):
        return self.title
