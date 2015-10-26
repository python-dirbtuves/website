from django_webtest import WebTest

from pylab.core.factories import EventFactory


class EventListTest(WebTest):

    def test_no_events_on_page(self):
        resp = self.app.get('/events/')
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'No events yet.' in resp.content)

    def test_event_list_on_page(self):
        EventFactory(title='Summer Python workshop')

        resp = self.app.get('/events/')
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'Summer Python workshop' in resp.content)
