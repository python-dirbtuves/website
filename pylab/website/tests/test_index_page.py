import django_webtest

import django.contrib.auth.models as auth_models


class IndexPageTests(django_webtest.WebTest):
    def setUp(self):
        super().setUp()
        auth_models.User.objects.create_user('u1')

    def test_index_page_with_anonymous_user(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_int, 200)

    def test_index_page_with_logged_in_user(self):
        resp = self.app.get('/', user='u1')
        self.assertEqual(resp.status_int, 200)
