import datetime

from django_webtest import WebTest

from django.contrib.auth.models import User

from pylab.core.models import Event


class EventAdminTests(WebTest):

    def test_add_event(self):
        now = datetime.datetime.now()

        user = User.objects.create_superuser('admin', 'admin@example.com', 'secret')

        self.assertEqual(Event.objects.count(), 0)

        resp = self.app.get('/admin/core/event/add/', user='admin')
        resp.form['title'] = 'Summer Python Workshop'
        resp.form['starts_0'] = now.strftime('%Y-%m-%d')
        resp.form['starts_1'] = now.strftime('%H:%M:%S')
        resp = resp.form.submit()

        self.assertEqual(resp.status_int, 302)
        self.assertEqual(Event.objects.count(), 1)

        event = Event.objects.get()
        self.assertEqual(event.author.pk, user.pk)
