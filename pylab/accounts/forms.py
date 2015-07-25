from django import forms
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
        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()
