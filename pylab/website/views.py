from django.utils.functional import curry

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext
from django.db.models import Sum

from pylab.core.models import Project, Event, Attendance, VotingPoll
from pylab.website.helpers import formrenderer
from pylab.website.helpers.decorators import superuser_required
from pylab.website.services import weeklyevents
import pylab.website.forms as website_forms


def landing_page(request):
    return render(request, 'website/index.html', {
        'projects': Project.objects.all(),
    })


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
    return render(request, 'website/about.html', {
        'events': Event.objects.all().exclude(parent_event=True),
    })


def event_details(request, year, month, day, slug):
    event = get_object_or_404(Event, starts__year=year, starts__month=month, starts__day=day, slug=slug)
    attendances = Attendance.objects.filter(event=event, response__in=[1, 2]).order_by('-response')
    if request.user.is_authenticated():
        try:
            instance = Attendance.objects.get(event=event, attendee=request.user)
        except Attendance.DoesNotExist:
            instance = Attendance(event=event, attendee=request.user)
        if request.method == 'POST':
            form = website_forms.AttendanceForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect(event)
        else:
            form = website_forms.AttendanceForm(instance=instance,
                                                initial={'response': instance.response if instance.response else 1})
        return render(request, 'website/event_details.html', {
            'event': event,
            'attendances': attendances,
            'form': formrenderer.render(request, form, title=ugettext('Are you coming?'), submit=ugettext('Submit'))
        })
    return render(request, 'website/event_details.html', {
        'event': event,
        'attendances': attendances,
    })


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


@login_required
def voting_page(request, voting_poll_slug):
    voting_poll = get_object_or_404(VotingPoll, slug=voting_poll_slug)
    total_points = 15
    ProjectPointsFormSet = modelformset_factory(
        Project,
        form=website_forms.ProjectPointsForm,
        formset=website_forms.BaseTotalPointsFormset,
        extra=0,
    )
    ProjectPointsFormSet.form = staticmethod(curry(
        website_forms.ProjectPointsForm,
        user=request.user,
        voting_poll=voting_poll))

    if request.method == 'POST':
        formset = ProjectPointsFormSet(request.POST, queryset=voting_poll.projects.all())
        if formset.is_valid():
            formset.save()
            messages.success(request, ugettext("Vote for „%s“ voting poll was saved successfully." % voting_poll))
            return redirect(voting_poll)
    else:
        formset = ProjectPointsFormSet(queryset=voting_poll.projects.all())

    return render(request, 'website/voting_page.html', {
        'voting_poll': voting_poll,
        'formset': formset,
        'total_points': total_points,
    })


@login_required
def voting_poll_details(request, voting_poll_slug):
    voting_poll = get_object_or_404(VotingPoll, slug=voting_poll_slug)

    projects = Project.objects.filter(vote__voting_poll=voting_poll)
    projects = projects.annotate(Sum('vote__points')).order_by('-vote__points__sum')

    return render(request, 'website/voting_poll_details.html', {
        'voting_poll': voting_poll,
        'projects': projects,
    })


def voting_poll_list(request):
    return render(request, 'website/voting_poll_list.html', {
        'votingPolls': VotingPoll.objects.all(),
    })
