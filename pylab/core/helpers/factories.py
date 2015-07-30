import datetime

import faker


class FakerFactoryBoyWrapper(object):
    """Small wrapper around faker for factory boy.

    Usage:

        >>> from factory import LazyAttribute
        >>> from pylab.core.helpers.factories import fake
        >>> LazyAttribute(fake.company())  # doctest: +ELLIPSIS
        <factory.declarations.LazyAttribute object at 0x...>

    """

    def __init__(self):
        self.faker = faker.Factory.create()

    def __getattr__(self, name):
        faker_method = getattr(self.faker, name)

        def wrapper(*args, **kwargs):
            def func(obj=None):  # pylint: disable=unused-argument
                return faker_method(*args, **kwargs)
            return func

        return wrapper


fake = FakerFactoryBoyWrapper()  # pylint: disable=invalid-name


_now = datetime.datetime.utcnow()


def _get_timedelta_kwargs(**kwargs):
    return {k: v for k, v in kwargs.items() if k in {
        'days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours', 'weeks',
    }}


def _get_datetime_replace_kwargs(**kwargs):
    return {k: v for k, v in kwargs.items() if k in {
        'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond', 'tzinfo',
    }}


def _get_datetime(dt, date=False, **kwargs):
    if date:
        dt = dt.date()

    replace_kwargs = _get_datetime_replace_kwargs(**kwargs)
    if replace_kwargs:
        dt = dt.replace(**replace_kwargs)

    return dt


def now():

    def func(obj=None):  # pylint: disable=unused-argument
        return _now

    return func


def today():

    def func(obj=None):  # pylint: disable=unused-argument
        return _now.date()

    return func


def future(**kwargs):
    delta = datetime.timedelta(**_get_timedelta_kwargs(**kwargs))

    def func(obj=None):  # pylint: disable=unused-argument
        return _get_datetime(_now + delta, **kwargs)

    return func


def past(**kwargs):
    delta = datetime.timedelta(**_get_timedelta_kwargs(**kwargs))

    def func(obj=None):  # pylint: disable=unused-argument
        return _get_datetime(_now - delta, **kwargs)

    return func
