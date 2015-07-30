import datetime

from django.utils import timezone


def next_weekday(weekday, now=None):
    now = now or timezone.now()
    # http://stackoverflow.com/a/8708150/475477
    n = (weekday - now.weekday()) % 7  # mod-7 ensures we don't go backward in time
    return now + datetime.timedelta(days=n)
