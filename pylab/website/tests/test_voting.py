import datetime

from django_webtest import WebTest

from pylab.core.factories import UserFactory, VotingPollFactory, ProjectFactory
from pylab.core.models import Vote


class VotingTests(WebTest):

    def test_voting_and_voting_poll_details_page(self):
        u1 = UserFactory()
        u2 = UserFactory()

        p1 = ProjectFactory(author=u1)
        p2 = ProjectFactory(author=u1)

        vp = VotingPollFactory(author=u1)
        vp.projects.add(p1)
        vp.projects.add(p2)

        resp = self.app.get(vp.get_voting_url(), user=u1)
        self.assertEqual(resp.status_int, 200)

        time_before_vote = datetime.datetime.now()

        resp.form['form-0-points'].value = 3
        resp.form['form-1-points'].value = 2
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)

        time_after_vote = datetime.datetime.now()

        self.assertEqual(list(Vote.objects.filter(voter=u1).values_list('points', flat=True)), [3, 2])

        for v in Vote.objects.filter(voter=u1):
            self.assertLess(time_before_vote, v.voted)
            self.assertGreater(time_after_vote, v.voted)

        resp = self.app.get(vp.get_voting_url(), user=u2)
        self.assertEqual(resp.status_int, 200)

        time_before_vote = datetime.datetime.now()

        resp.form['form-0-points'].value = 6  # Vote points sum should be less or equal to 15
        resp.form['form-1-points'].value = 5
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)

        time_after_vote = datetime.datetime.now()

        self.assertEqual(list(Vote.objects.filter(voter=u2).values_list('points', flat=True)), [6, 5])

        for v in Vote.objects.filter(voter=u2):
            self.assertLess(time_before_vote, v.voted)
            self.assertGreater(time_after_vote, v.voted)

        resp = self.app.get(vp.get_absolute_url(), user=u1)
        self.assertEqual(resp.status_int, 200)

        self.assertTrue(b'9' in resp.content)
        self.assertTrue(b'7' in resp.content)
