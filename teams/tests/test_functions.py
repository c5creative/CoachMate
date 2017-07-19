from __future__ import unicode_literals
from unittest import skip, skipIf, skipUnless
from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

import teams.tests.test_setup as test
from teams.models import Week
import teams.functions as funct


class FunctionTests(TestCase):
    def test_get_monday_present(self):
        """
        Returns most recent Monday. To test, uncomment and change current_mon date.
        Tested and works.
        """
        week = test.create_week()
        week.populate()
        monday = funct.get_monday(week=week)
        current_mon = date(2017,7,10)
        self.assertEqual(monday, current_mon)

    def test_get_monday_previous(self):
        """
        Returns previous Monday. To test, uncomment and change previous_mon date.
        Tested and works.
        """
        week = test.create_week()
        week.populate()
        monday = funct.get_monday(week, 0)
        previous_mon = date(2017,7,3)
        self.assertEqual(monday, previous_mon)

    def test_get_monday_next(self):
        """
        Returns next Monday. To test, uncomment and change next_mon date.
        Tested and works.
        """
        week = test.create_week()
        week.populate()
        monday = funct.get_monday(week, 1)
        next_mon = date(2017,7,17)
        self.assertEqual(monday, next_mon)

    def test_date_range(self):
        """
        Yields all dates in a given week.
        """
        dates = [
            date(2017,7,10),
            date(2017,7,11),
            date(2017,7,12),
            date(2017,7,13),
            date(2017,7,14),
            date(2017,7,15),
            date(2017,7,16),
        ]
        returned_dates = []
        for day in funct.date_range(date(2017,7,10), date(2017,7,16)):
            returned_dates.append(day)
        self.assertEqual(dates, returned_dates)

    def test_check_present_with_no_weeks(self):
        """
        Returns None.
        """
        out = funct.check_present()
        self.assertFalse(out)

    def test_check_present_with_present_week(self):
        """
        Sets the boolean value of the correct present week to True and all others
        to False. The function also returns True.
        """
        mon_present = funct.get_monday(n=None)
        mon_previous = funct.get_monday(n=0)
        mon_next = funct.get_monday(n=1)
        week1 = test.create_week(monday=mon_present)
        week1.populate()
        week2 = test.create_week(monday=mon_previous)
        week2.populate()
        week3 = test.create_week(monday=mon_next, present=True)
        week3.populate()

        out = funct.check_present()

        for week in [week1, week2, week3]:
            week.refresh_from_db()

        self.assertTrue(out)
        self.assertTrue(week1.present)
        self.assertFalse(week2.present)
        self.assertFalse(week3.present)

    def test_check_present_with_no_present_week(self):
        """
        Sets all current boolean values to False and returns False.
        """
        week1 = test.create_week(monday=(date.today() - relativedelta(days=7)))
        week1.populate()
        week2 = test.create_week(monday=(date.today() + relativedelta(days=7)), present=True)
        week2.populate()

        out = funct.check_present()

        for week in [week1, week2]:
            week.refresh_from_db()

        self.assertTrue(out)
        self.assertFalse(week1.present)
        self.assertFalse(week2.present)
