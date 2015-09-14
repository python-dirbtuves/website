import factory
import factory.django

from django.contrib.auth.models import User

from pylab.core.models import Event, Project, VotingPoll
from pylab.core.helpers.factories import fake, future


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(fake.user_name())


class SuperUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(fake.user_name())
    is_staff = True
    is_superuser = True


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event
        django_get_or_create = ('slug',)

    author = factory.SubFactory(UserFactory)
    parent_event = None
    event_type = Event.OTHER
    slug = factory.LazyAttribute(fake.slug())
    title = factory.LazyAttribute(fake.company())
    description = factory.LazyAttribute(fake.sentence())
    starts = factory.LazyAttribute(future(days=1, hour=18, minute=0, second=0))
    ends = factory.LazyAttribute(future(days=1, hour=20, minute=0, second=0))


class ProjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Project
        django_get_or_create = ('slug',)

    author = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(fake.company())
    slug = factory.LazyAttribute(fake.slug())
    description = factory.LazyAttribute(fake.sentence())


class VotingPollFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = VotingPoll
        django_get_or_create = ('slug',)

    author = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(fake.company())
    slug = factory.LazyAttribute(fake.slug())
    description = factory.LazyAttribute(fake.sentence())
