import datetime

from django_webtest import WebTest

from pylab.core.models import Event
from pylab.core.factories import EventFactory


class AboutPageTests(WebTest):

    def test_no_events_on_about_page(self):
        resp = self.app.get('/about/')
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'No events yet.' in resp.content)

    def test_event_list_on_about_page(self):
        EventFactory(
            event_type=Event.WEEKLY_MEETING,
            title='Summer Python workshop',
            slug='python-workshop',
            starts=datetime.datetime(2015, 7, 30, 18, 0),
            ends=datetime.datetime(2015, 7, 30, 20, 0),
        )

        resp = self.app.get('/about/')
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'Summer Python workshop' in resp.content)
