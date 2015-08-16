from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pylab.core.models import Project, Event, Attendance
from pylab.website.helpers import formrenderer
from pylab.website.helpers.decorators import superuser_required
from pylab.website.services import weeklyevents
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


def event_details(request, year, month, day, slug):
    event = get_object_or_404(Event, starts__year=year, starts__month=month, starts__day=day, slug=slug)
    attendance = Attendance.objects.filter(event=event)
    if request.method == 'POST':
        form = website_forms.AttendanceForm(request.POST)
        if form.is_valid():
            instance = Attendance.objects.get(event=event, attendee=request.user)
            instance.response = form.cleaned_data['response']
            instance.save()
            return redirect(event)
    else:
        if request.user.is_authenticated():
            instance, created = Attendance.objects.get_or_create(event=event, attendee=request.user,  # pylint: disable=unused-variable
                                                                 defaults={'response': 1})
            form = website_forms.AttendanceForm(instance=instance, initial={'response': instance.response})
            return render(request, 'website/event_details.html',
                          {'event': event,
                           'attendances': attendance,
                           'form': formrenderer.render(request, form, title=ugettext('Are you coming?'),
                                                       submit=ugettext('Submit'))})
        else:
            return render(request, 'website/event_details.html', {'event': event, 'attendances': attendance})


@superuser_required
def create_weekly_event(request, year, month, day, slug):
    parent_event = get_object_or_404(Event, starts__year=year, starts__month=month, starts__day=day, slug=slug)

    if request.method == 'POST':
        form = website_forms.NextWeeklyEventForm(parent_event, request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            weeklyevents.save(request, parent_event, event)
            return redirect(event.get_absolute_url())
    else:
        form = website_forms.NextWeeklyEventForm(parent_event, initial=weeklyevents.get_initial_values())

    return render(request, 'website/weekly_event_form.html', {
        'form': formrenderer.render(
            request, form,
            title=parent_event.title,
            description=ugettext("Create new weekly event for \"%s\".") % parent_event.title,
            submit=ugettext("Announce"),
        ),
    })
