import datetime

from django_webtest import WebTest

from django.contrib.auth.models import User

from django_comments.models import Comment

from pylab.core.models import Project


class CommentsTests(WebTest):

    def setUp(self):
        self.user = User.objects.create_user('u1')
        self.project = Project.objects.create(
            author=self.user,
            title='Test project',
            description='Description',
            created='2015-08-13'
        )

    def test_add_comment(self):
        resp = self.app.get('/projects/test-project/', user=self.user)
        now = datetime.datetime.now()
        comment = Comment.objects.create(
            user=self.user,
            comment='new comment',
            submit_date=now,
            object_pk=self.project.id,
            content_type_id=self.project.id,
            site_id=1,
        )
        comment.save()
        resp = self.app.get('/projects/test-project/', user=self.user)
        self.assertEqual(resp.status_int, 200)

        self.assertEqual(
            list(Comment.objects.values_list('comment')),
            [('new comment',)]
        )
