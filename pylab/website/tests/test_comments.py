from django_webtest import WebTest

from django.contrib.auth.models import User

from django_comments.models import Comment

from pylab.core.models import Project


class CommentsTests(WebTest):

    def setUp(self):
        self.user = User.objects.create_user('u1', email='test@example.com')
        self.project = Project.objects.create(
            author=self.user,
            title='Test project',
            description='Description',
            created='2015-08-13'
        )

    def get_form(self, resp, form_type):
        for form in resp.forms.values():
            if form['content_type'].value == form_type:
                return form

    def test_add_comment(self):
        # Add a comment to project
        resp = self.app.get('/projects/test-project/', user=self.user)
        resp.form['comment'] = 'new comment'
        resp = resp.form.submit()

        resp = self.app.get('/projects/test-project/', user=self.user)
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'new comment' in resp.content)
        self.assertEqual(
            list(Comment.objects.values_list('comment')),
            [('new comment',)]
        )

        # Add reply to first comment
        resp = self.app.get('/projects/test-project/', user=self.user)
        self.assertEqual(resp.status_int, 200)

        reply_form = self.get_form(resp, 'django_comments.comment')
        reply_form['comment'] = 'My reply to the first comment'
        reply_form.submit()
        self.assertEqual(resp.status_int, 200)

        resp = self.app.get('/projects/test-project/', user=self.user)
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'My reply to the first comment' in resp.content)
        self.assertTrue(Comment.objects.filter(comment='My reply to the first comment').exists())

        # Add one more top level comment
        resp = self.app.get('/projects/test-project/', user=self.user)
        self.assertEqual(resp.status_int, 200)

        reply_form = self.get_form(resp, 'core.project')
        reply_form['comment'] = 'Second project comment'
        reply_form.submit()
        self.assertEqual(resp.status_int, 200)

        resp = self.app.get('/projects/test-project/', user=self.user)
        self.assertEqual(resp.status_int, 200)
        self.assertTrue(b'Second project comment' in resp.content)
        self.assertTrue(Comment.objects.filter(comment='Second project comment').exists())
