from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.utils.translation import ugettext
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import pylab.accounts.helpers.allauth as allauth_helpers
import pylab.accounts.forms as accounts_forms
from pylab.website.helpers import formrenderer


def login(request):
    openid_providers, form = allauth_helpers.get_openid_providers(request)
    if form:
        return allauth_helpers.openid_login(request, form)
    else:
        return render(request, 'accounts/login.html', {
            'auth_providers': allauth_helpers.get_auth_providers(request),
            'openid_providers': openid_providers,
        })


def logout(request):
    auth.logout(request)
    return redirect('project-list')


@login_required
def settings(request):
    if request.method == 'POST':
        form = accounts_forms.UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, ugettext("Settings were saved succesfully."))
            return redirect('accounts_settings')
    else:
        form = accounts_forms.UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/settings.html', {
        'form': formrenderer.render(request, form, title=ugettext("Profile settings"), submit=ugettext("Save")),
    })
