import datetime
import pytz

from pylab.core.models import Event
from pylab.website.utils.dates import next_weekday


def save(request, parent_event: Event, event: Event):
    """Save weekly event."""
    event.author = request.user
    event.parent_event = parent_event
    event.event_type = Event.WEEKLY_MEETING
    event.hide_time = False
    event.save()
    event.description = event.description.format(link=request.build_absolute_uri(event.get_absolute_url()))
    event.save()
    return event


def get_initial_values() -> dict:
    """Returns initial data for weekly event form."""
    time = datetime.time(18, tzinfo=pytz.timezone('Europe/Vilnius'))
    next_monday = datetime.datetime.combine(next_weekday(0), time)

    return {
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
    }
