import django_webtest

import django.contrib.auth.models as auth_models

from pylab.core.models import Project


class StaticPagesTests(django_webtest.WebTest):
    def setUp(self):
        super().setUp()
        auth_models.User.objects.create_user('u1')

    def test_project_creation_and_editing(self):
        resp = self.app.get('/projects/create/', user='u1')
        self.assertEqual(resp.status_int, 200)

        resp.form['title'] = 'Test project'
        resp.form['description'] = 'Test description'
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)

        resp = self.app.get('/projects/test-project/', user='u1')
        self.assertEqual(resp.status_int, 200)

        self.assertEqual(
            list(Project.objects.values_list('title', 'description')),
            [('Test project', 'Test description')]
        )

        resp = self.app.get('/projects/test-project/update/', user='u1')
        resp.form['title'] = 'Test project2'
        resp.form['description'] = 'Test description2'
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)

        self.assertEqual(
            list(Project.objects.values_list('title', 'description')),
            [('Test project2', 'Test description2')]
        )

        resp = self.app.get('/projects/test-project/', user='u1')
        self.assertEqual(resp.status_int, 200)
