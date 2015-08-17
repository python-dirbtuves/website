import datetime

from django.test import TestCase

from django.contrib.auth.models import User

from django_comments.models import Comment

from pylab.core.models import Project


class CommentsTests(TestCase):

    def test_add_comment(self):
        user = User.objects.create_user('user1')
        project = Project.objects.create(
            author=user,
            title='Test project',
            description='Description',
            created='2015-08-13'
        )
        now = datetime.datetime.now()
        comment = Comment.objects.create(
            user_name='user2',
            comment='test comment',
            submit_date=now,
            object_pk=project.id,
            content_type_id=project.id,
            site_id=1,
        )
        comment.save()
        resp = self.client.post('/projects/test-project/', {'comment': comment})

        self.assertEqual(resp.status_code, 200)
#       self.assertContains(resp, 'test comment')
