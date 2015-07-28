from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pylab.core.models import Project
from pylab.website.helpers import formrenderer
import pylab.website.forms as website_forms


def project_list(request):
    return render(request, 'website/project_list.html', {
        'projects': Project.objects.all(),
    })


def project_details(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    return render(request, 'website/project_details.html', {
        'project': project,
        'can_update': request.user.is_authenticated() and (request.user.is_superuser or project.author == request.user)
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = website_forms.ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request, ugettext("Project „%s“ created." % project))
            return redirect(project)
    else:
        form = website_forms.ProjectForm()

    return render(request, 'website/project_form.html', {
        'form': formrenderer.render(request, form, title=ugettext('Suggest new project'), submit=ugettext('Submit')),
    })


@login_required
def project_update(request, project_slug):
    if request.user.is_superuser:
        project = get_object_or_404(Project, slug=project_slug)
    else:
        project = get_object_or_404(Project, slug=project_slug, author=request.user)

    if request.method == 'POST':
        form = website_forms.ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, ugettext("Project „%s“ updated." % project))
            return redirect(project)
    else:
        form = website_forms.ProjectForm(instance=project)

    return render(request, 'website/project_form.html', {
        'form': formrenderer.render(request, form, title=project.title, submit=ugettext('Submit')),
    })


def about(request):
    return render(request, 'website/about.html', {})
