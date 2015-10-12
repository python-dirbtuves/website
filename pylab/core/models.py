from autoslug import AutoSlugField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    PROPOSED = 0
    IN_PROGRESS = 1
    SUSPENDED = 2
    IMPLEMENTED = 3
    PROJECT_STATUS_CHOICES = (
        (PROPOSED, _("Proposed")),
        (IN_PROGRESS, _('In progress')),
        (SUSPENDED, _('Suspended')),
        (IMPLEMENTED, _('Implemented')),
    )

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User)
    slug = AutoSlugField(populate_from='title')
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    url = models.URLField(_("URL"), blank=True)
    status_description = models.TextField(_("Status Description"), blank=True)
    status = models.PositiveSmallIntegerField(choices=PROJECT_STATUS_CHOICES, default=PROPOSED)

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
    attendees = models.ManyToManyField(User, through='Attendance', related_name='attendees')

    class Meta:
        unique_together = ('starts', 'slug')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-details', args=[self.starts.year, self.starts.month, self.starts.day, self.slug])


class VotingPoll(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    author = models.ForeignKey(User)
    slug = AutoSlugField(populate_from='title')
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    projects = models.ManyToManyField(Project)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('voting-poll-details', args=[self.slug])

    def get_voting_url(self):
        return reverse('voting-page', args=[self.slug])


class Vote(models.Model):
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    voted = models.DateTimeField(null=True)
    voting_poll = models.ForeignKey(VotingPoll)
    voter = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    points = models.PositiveIntegerField(_("Points"), null=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.voting_poll.title, self.voter.get_full_name() or self.voter.get_username())


class Attendance(models.Model):
    NO = 3
    YES = 2
    MAYBE = 1
    ATTENDANCE_CHOICES = (
        (NO, _('No')),
        (YES, _('Yes')),
        (MAYBE, _('Maybe'))
    )

    attendee = models.ForeignKey(User)
    event = models.ForeignKey('Event')
    response = models.PositiveSmallIntegerField(choices=ATTENDANCE_CHOICES, null=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __str__(self):
        return '%s : %s : %s' % (self.event.title, self.attendee.username, self.get_response_display())

    class Meta:
        unique_together = ('attendee', 'event')
