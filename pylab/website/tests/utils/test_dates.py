import datetime
import unittest

from pylab.website.utils.dates import next_weekday


class NextWeekdayTests(unittest.TestCase):
    def assertWeekday(self, weekday, date, expected):
        result = next_weekday(weekday, datetime.datetime(*date))
        self.assertEqual(datetime.datetime(*expected), result)

    def test_next_weekday(self):
        self.assertWeekday(0, (2015, 7, 27), (2015, 7, 27))  # Monday
        self.assertWeekday(0, (2015, 7, 28), (2015, 8, 3))   # Tuesday
        self.assertWeekday(0, (2015, 7, 29), (2015, 8, 3))   # Wednesday
        self.assertWeekday(0, (2015, 7, 30), (2015, 8, 3))   # Thursday
        self.assertWeekday(0, (2015, 7, 31), (2015, 8, 3))   # Friday
        self.assertWeekday(0, (2015, 8, 1), (2015, 8, 3))    # Saturday
        self.assertWeekday(0, (2015, 8, 2), (2015, 8, 3))    # Sunday
