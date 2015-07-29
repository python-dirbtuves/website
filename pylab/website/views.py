import datetime
import pytz

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pylab.core.models import Project, Event
from pylab.website.helpers import formrenderer
from pylab.website.utils.dates import next_weekday
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
    return render(request, 'website/event_details.html', {'event': event})


def create_monday_event(request, year, month, day, slug):
    parent_event = get_object_or_404(Event, starts__year=year, starts__month=month, starts__day=day, slug=slug)

    if request.method == 'POST':
        form = website_forms.NextMondayEvent(parent_event, request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.parent_event = parent_event
            event.event_type = Event.WEEKLY_MEETING
            event.hide_time = False
            event.save()
            event.description = event.description.format(link=request.build_absolute_uri(event.get_absolute_url()))
            event.save()
            return redirect(event.get_absolute_url())
    else:
        time = datetime.time(18, tzinfo=pytz.timezone('Europe/Vilnius'))
        next_monday = datetime.datetime.combine(next_weekday(0), time)
        form = website_forms.NextMondayEvent(parent_event, initial={
            'title': "Python dirbtuvės %s" % next_monday.strftime('%Y-%m-%d'),
            'starts': next_monday,
            'ends': next_monday + datetime.timedelta(hours=2),
            'address': "M. K. Čiurlionio 13-1, Vilnius",
            'osm_map_link': 'http://www.openstreetmap.org/export/embed.html?bbox=25.25977849960327%2C54.68112590686655%2C25.266462564468384%2C54.68386427291551&layer=mapnik&marker=54.68249356237776%2C25.263120532035828',
            'description': '\n'.join([
                'As always, same place, same time.',
                '',
                'Please register if you planning to attend:',
                '',
                '{link}',
                '',
                '--',
                'pylab.lt',
            ]),
        })

    return render(request, 'website/monday_event_form.html', {
        'form': formrenderer.render(
            request, form,
            title=parent_event.title,
            description=ugettext("Create new weekly event for \"%s\".") % parent_event.title,
            submit=ugettext("Announce"),
        ),
    })
