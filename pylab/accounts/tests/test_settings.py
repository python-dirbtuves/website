import django_webtest

import django.contrib.auth.models as auth_models

import pylab.accounts.models as accounts_models


class SettingsTests(django_webtest.WebTest):
    def setUp(self):
        super().setUp()
        auth_models.User.objects.create_user('u1')

    def test_user_settings(self):
        resp = self.app.get('/accounts/settings/', user='u1')
        resp.form['first_name'] = 'My'
        resp.form['last_name'] = 'Name'
        resp.form['email'] = ''
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)
        # User settings were saved correctly
        self.assertEqual(list(auth_models.User.objects.values_list('first_name', 'last_name', 'email')), [
            ('My', 'Name', ''),
        ])
        # User profile was created for new user and language is not selected
        self.assertEqual(list(accounts_models.UserProfile.objects.values_list('language')), [('',), ])

    def test_userprofile_settings(self):
        resp = self.app.get('/accounts/settings/', user='u1')
        resp.form['language'] = 'en'
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)
        # Language setting was saved correctly
        self.assertEqual(list(accounts_models.UserProfile.objects.values_list('language')), [('en',), ])

    def test_user_profile_locale_middleware(self):
        resp = self.app.get('/accounts/settings/', user='u1')
        resp.form['language'] = 'en'
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)
        resp = self.app.get('/accounts/settings/', user='u1')
        # Website interface is displayed in english
        self.assertTrue(b'Save' in resp.content)

        resp.form['language'] = 'lt'
        resp = resp.form.submit()
        self.assertEqual(resp.status_int, 302)
        resp = self.app.get('/accounts/settings/', user='u1')
        # Website interface is displayed in lithuanian
        self.assertTrue(b'Saugoti' in resp.content)
