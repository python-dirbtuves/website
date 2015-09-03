import datetime

from django_webtest import WebTest
from django.contrib.auth.models import User

from pylab.core.models import Event


class AboutPageTests(WebTest):

    def setUp(self):
        self.user = User.objects.create(username='u1')

    def test_no_events_on_about_page(self):
        resp = self.app.get('/about/')
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'No events yet.' in resp.content)

    def test_event_list_on_about_page(self):
        Event.objects.create(
            author=self.user,
            starts=datetime.datetime(2015, 9, 3),
            ends=datetime.datetime(2015, 9, 3),
            title='Test title',
            osm_map_link='http://openstreetmap.org/',
            description='Test description',
        )
        resp = self.app.get('/about/')
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'Test title' in resp.content)
