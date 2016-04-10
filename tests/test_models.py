#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_acp-calendar
------------

Tests for `acp-calendar` models module.
"""
import datetime

from django.test import TestCase

from acp_calendar import models
from acp_calendar.initial_data import get_holiday_type_list
from acp_calendar.models import HolidayType, ACPHoliday, FiscalYear


class TestFiscalYear(TestCase):

    def test__create(self):
        fy = FiscalYear(2016)
        self.assertEqual('FY16', str(fy))
        self.assertEqual(datetime.date(2015, 10, 1), fy.start_date)
        self.assertEqual(datetime.date(2016, 9, 30), fy.end_date)

    def test__str(self):
        fy = FiscalYear(2014, display='AF%s')
        self.assertEqual('AF14', str(fy))

    def test_create_from_date(self):
        cdate = datetime.date(2013, 10, 1)
        fy = FiscalYear.create_from_date(cdate)
        self.assertEqual('FY14', str(fy))

class TestHolidayType(TestCase):

    def setUp(self):
        pass

    def test_create(self):
        loaded_holiday_types = len(get_holiday_type_list())
        data = {'name': 'My Holiday'}
        HolidayType.objects.create(**data)
        self.assertEqual(11, loaded_holiday_types)
        self.assertEqual(1 + loaded_holiday_types, HolidayType.objects.count())

    def tearDown(self):
        pass


class TestACPHoliday(TestCase):

    def setUp(self):
        pass

    def test_load_initial(self):
        loaded_holidays = len(get_holiday_type_list())
        self.assertEqual(11, loaded_holidays)

    def test_days_in_range_generator(self):
        start_date = datetime.date(2016, 1,1)
        end_date = datetime.date(2016,1,31)
        jan_days = list(ACPHoliday.days_in_range_generator(start_date, end_date))
        self.assertEqual(31, len(jan_days))
        self.assertEqual(jan_days[0], start_date)
        self.assertEqual(jan_days[30], end_date)

    def test_get_working_days(self):
        start_date = datetime.date(2016, 1,1)
        end_date = datetime.date(2016,1,31)
        working_days = ACPHoliday.get_working_days(start_date, end_date)
        self.assertEqual(19, working_days)

    def test_get_working_days_no_work(self):
        start_date = datetime.date(2016, 1,1)
        end_date = datetime.date(2016,1,2)
        working_days = ACPHoliday.get_working_days(start_date, end_date)
        self.assertEqual(0, working_days)

    def test_validate_dates_last_holiday(self):
        first_holiday = ACPHoliday.objects.all().first()
        last_holiday = ACPHoliday.objects.all().last()
        try:
            ACPHoliday.validate_dates(first_holiday.date, last_holiday.date + datetime.timedelta(days=1))
            self.fail('Value error should have been raised')
        except ValueError as e:
            self.assertEqual('End date exceed the last registered holiday', str(e))

    def test_validate_dates_first_holiday(self):
        first_holiday = ACPHoliday.objects.all().first()
        last_holiday = ACPHoliday.objects.all().last()
        try:
            ACPHoliday.validate_dates(first_holiday.date - datetime.timedelta(days=1), last_holiday.date)
            self.fail('Value error should have been raised')
        except ValueError as e:
            self.assertEqual('Start date precedes the first registered holiday', str(e))


    def tearDown(self):
        pass
