from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth.models as auth_models

import pylab.accounts.models as accounts_models


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)
    email = forms.EmailField(label=_('Email address'), required=False)

    class Meta:
        model = accounts_models.UserProfile
        fields = ('first_name', 'last_name', 'email', 'language')
        help_texts = {
            'email': _(
                "Will be used for communication. If you want not to get any emails, leave this field empty."
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['language'].choices = [("", _("Default")),] + self.fields["language"].choices[1:]
        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()


class SignupForm(forms.ModelForm):
    language = forms.ChoiceField(label=_('Language'), required=False,
                                 choices=[("", _("Default")),] + list(settings.LANGUAGES))

    class Meta:
        model = auth_models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'language')
        help_texts = {
            'email': _(
                "Will be used for communication. If you want not to get any emails, leave this field empty."
            ),
        }

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        user.profile.language = self.cleaned_data['language']
        user.profile.save()
