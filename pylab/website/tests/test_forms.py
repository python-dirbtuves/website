import datetime

from django.test import TestCase

from pylab.core.models import Event
from pylab.core.factories import EventFactory
from pylab.website.forms import NextWeeklyEventForm


class NextWeeklyEventFormTests(TestCase):

    def test_duplicates(self):
        parent_event = EventFactory(event_type=Event.PROJECT_DEVELOPMENT)

        EventFactory(
            parent_event=parent_event,
            event_type=Event.WEEKLY_MEETING,
            title='Python workshop',
            slug='python-workshop',
            starts=datetime.datetime(2015, 7, 30, 18, 0),
            ends=datetime.datetime(2015, 7, 30, 20, 0),
        )

        form = NextWeeklyEventForm(parent_event, {
            'title': 'Python workshop',
            'starts': '2015-07-30 18:00',
            'ends': '2015-07-30 20:00',
            'address': '',
            'osm_map_link': '',
            'description': '',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), ["Event with same title on same day already exist."])
