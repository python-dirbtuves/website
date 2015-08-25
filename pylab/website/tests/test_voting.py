import datetime

from django_webtest import WebTest
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from pylab.core.models import Project, VotingPoll, Vote


class VotingTests(WebTest):

    def setUp(self):
        super().setUp()
        self.u1 = User.objects.create_user('u1')

    def test_voting_page(self):
        p1 = Project.objects.create(author=self.u1, title='Test title 1', description='Test description')
        p2 = Project.objects.create(author=self.u1, title='Test title 2', description='Test description')

        vp = VotingPoll.objects.create(author=self.u1, title='Test voting poll', description='Test description')

        Vote.objects.create(voter=self.u1, voting_poll=vp, project=p1)
        Vote.objects.create(voter=self.u1, voting_poll=vp, project=p2)

        resp = self.app.get('/vote/test-voting-poll/', user=self.u1)
        self.assertEqual(resp.status_int, 200)

        time_before_vote = datetime.datetime.now()

        resp.form['form-0-points'].value = 3
        resp.form['form-1-points'].value = 2
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)

        time_after_vote = datetime.datetime.now()

        self.assertEqual(list(Vote.objects.values_list('points', flat=True)), [3, 2])

        for v in Vote.objects.all():
            self.assertLess(time_before_vote, v.voted)
            self.assertGreater(time_after_vote, v.voted)

        resp = self.app.get('/vote/test-voting-poll/', user=self.u1)
        self.assertEqual(resp.status_int, 200)

        time_before_vote = datetime.datetime.now()

        resp.form['form-0-points'].value = 30  # Vote points sum should be less or equal to 15
        resp.form['form-1-points'].value = 20
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 200)

    def test_voting_poll_list_with_anonymous_user(self):
        resp = self.app.get(reverse('voting-poll-list'))
        self.assertEqual(resp.status_int, 200)

    def test_voting_poll_list_with_logged_user(self):
        resp = self.app.get(reverse('voting-poll-list'), user=self.u1)
        self.assertEqual(resp.status_int, 200)
