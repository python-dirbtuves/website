import datetime
import mock

import django_webtest

from pylab.core.models import Event
from pylab.core.factories import EventFactory, UserFactory


class MondayEventTests(django_webtest.WebTest):

    def setUp(self):
        super().setUp()
        UserFactory(username='user')
        self.event = EventFactory(event_type=Event.PROJECT_DEVELOPMENT)

    @mock.patch('pylab.website.views.next_weekday', autospec=True)
    def test_success(self, next_weekday):
        next_weekday.return_value = datetime.datetime(2015, 8, 3)

        resp = self.app.get('%screate-next-monday-event/' % self.event.get_absolute_url(), user='user')
        resp.form.submit()

        event = self.event.event_set.get()
        self.assertEqual(event.title, 'Python dirbtuvės 2015-08-03')
