import datetime

from django_webtest import WebTest

from django.contrib.auth.models import User

from pylab.core.models import Project, VotingPoll, Vote


class VotingTests(WebTest):

    def test_voting_page(self):
        u1 = User.objects.create(username='u1')

        p1 = Project.objects.create(author=u1, title='Test title 1', description='Test description')
        p2 = Project.objects.create(author=u1, title='Test title 2', description='Test description')

        vp = VotingPoll.objects.create(author=u1, title='Test voting poll', description='Test description')

        Vote.objects.create(voter=u1, voting_poll=vp, project=p1)
        Vote.objects.create(voter=u1, voting_poll=vp, project=p2)

        resp = self.app.get('/vote/test-voting-poll/', user='u1')
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

        resp = self.app.get('/vote/test-voting-poll/', user='u1')
        self.assertEqual(resp.status_int, 200)

        time_before_vote = datetime.datetime.now()

        resp.form['form-0-points'].value = 30  # Vote points sum should be less or equal to 15
        resp.form['form-1-points'].value = 20
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 200)

    def test_voting_poll_details(self):
        u1 = User.objects.create(username='u1')
        u2 = User.objects.create(username='u2')

        p1 = Project.objects.create(author=u1, title='Test title 1', description='Test description')
        p2 = Project.objects.create(author=u1, title='Test title 2', description='Test description')

        vp = VotingPoll.objects.create(author=u1, title='Test voting poll', description='Test description')

        Vote.objects.create(voter=u1, voting_poll=vp, project=p1, points=1)
        Vote.objects.create(voter=u1, voting_poll=vp, project=p2, points=2)
        Vote.objects.create(voter=u2, voting_poll=vp, project=p1, points=3)
        Vote.objects.create(voter=u2, voting_poll=vp, project=p2, points=4)

        resp = self.app.get('/voting-poll/test-voting-poll/', user='u1')

        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'4' in resp.content)
        self.assertTrue(b'6' in resp.content)
