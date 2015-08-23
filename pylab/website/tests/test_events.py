import datetime

from django_webtest import WebTest

from django.contrib.auth.models import User, AnonymousUser

from pylab.core.models import Event


class EventTests(WebTest):

    def setUp(self):
        self.user = User.objects.create(username='u1')
        Event.objects.create(
            author=self.user,
            starts=datetime.datetime(2015, 7, 29),
            ends=datetime.datetime(2015, 7, 30),
            title='Test title',
            osm_map_link='http://openstreetmap.org/',
            description='Test description',
        )

    def test_event_details_page(self):

        resp = self.app.get('/events/2015/07/29/test-title/', user=AnonymousUser())

        self.assertEqual(resp.status_int, 200)

        resp = self.app.get('/events/2015/07/29/test-title/', user=self.user)

        self.assertEqual(resp.status_int, 200)

    def test_event_response(self):
        resp = self.app.get('/events/2015/07/29/test-title/', user=self.user)
        form = resp.form
        form['response'] = 2  # Yes
        resp = form.submit().follow()
        print(resp)
        self.assertEqual(resp.status_int, 200)
        assert '<li>u1 <span>Yes</span></li>' in resp
