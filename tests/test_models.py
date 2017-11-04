#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_acp-calendar
------------

Tests for `acp-calendar` models module.
"""
import datetime
import os
from unittest import mock

from django.test import TestCase


from django.test import override_settings

from acp_calendar.initial_data import get_holiday_type_list, get_holidays_list
from acp_calendar.models import HolidayType, ACPHoliday, FiscalYear, ACPCalendarException

import datetime


from .utils import TestOutputMixin

real_datetime_class = datetime.datetime


def mock_datetime(target, datetime_module):
    class DatetimeSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

        @classmethod
        def today(cls):
            return target

    # Python2 & Python3-compatible metaclass
    MockedDatetime = DatetimeSubclassMeta('datetime', (BaseMockedDatetime,), {})

    return mock.patch.object(datetime_module, 'datetime', MockedDatetime)


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

    def test_create_from_date_2(self):
        cdate = datetime.date(2014, 9, 1)
        fy = FiscalYear.create_from_date(cdate)
        self.assertEqual('FY14', str(fy))

    def test_create_from_date_datetime(self):
        cdate = datetime.datetime(2013, 10, 1, 0, 0, 0)
        fy = FiscalYear.create_from_date(cdate)
        self.assertEqual('FY14', str(fy))

    @mock.patch('django.utils.timezone.now')
    def test_current_fiscal_year(self, mock_now):
        mock_now.return_value = datetime.datetime(2013, 10, 1, 0, 0, 0)
        fy = FiscalYear.current_fiscal_year()
        self.assertEqual('FY14', str(fy))



class TestHolidayType(TestCase):

    def setUp(self):
        pass

    def test_create(self):
        loaded_holiday_types = len(get_holiday_type_list())
        data = {'name': 'My Holiday'}
        HolidayType.objects.create(**data)
        self.assertEqual(12, loaded_holiday_types)
        self.assertEqual(1 + loaded_holiday_types, HolidayType.objects.count())

    def test_str(self):
        navidad = HolidayType.objects.get(short_name='navidad')
        self.assertEqual('Navidad', str(navidad))

    def tearDown(self):
        pass


class TestACPHoliday(TestOutputMixin, TestCase):

    def setUp(self):
        pass

    def test_str(self):
        holiday = ACPHoliday.objects.first()
        self.assertEqual('2006-01-01 Año Nuevo', str(holiday))

    def test_load_initial(self):
        loaded_holidays = len(get_holidays_list())
        self.assertEqual(144, ACPHoliday.objects.count())
        self.assertEqual(datetime.date(2006, 1,1), ACPHoliday.objects.first().date)
        self.assertEqual(datetime.date(2018, 12,25), ACPHoliday.objects.last().date)


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

    def test_get_working_days_wrong_dates(self):
        start_date = datetime.date(2016, 1, 5)
        end_date = datetime.date(2016, 1, 2)
        try:
            working_days = ACPHoliday.get_working_days(start_date, end_date)
            self.fail('Did not throw Value error')
        except ACPCalendarException as e:
            self.assertEqual('Start date cannot occur after end date', str(e))

    def test_validate_dates_last_holiday(self):
        first_holiday = ACPHoliday.objects.all().first()
        last_holiday = ACPHoliday.objects.all().last()
        try:
            ACPHoliday.validate_dates(first_holiday.date, last_holiday.date + datetime.timedelta(days=1))
            self.fail('Value error should have been raised')
        except ACPCalendarException as e:
            self.assertEqual('End date exceed the last registered holiday', str(e))

    def test_validate_dates_first_holiday(self):
        first_holiday = ACPHoliday.objects.all().first()
        last_holiday = ACPHoliday.objects.all().last()
        try:
            ACPHoliday.validate_dates(first_holiday.date - datetime.timedelta(days=1), last_holiday.date)
            self.fail('Value error should have been raised')
        except ACPCalendarException as e:
            self.assertEqual('Start date precedes the first registered holiday', str(e))

    def test_week_end_days(self):
        start_date = datetime.date(2016, 1, 1)
        end_date = datetime.date(2016, 1, 31)
        week_end_days = ACPHoliday.week_end_days(start_date, end_date)
        self.assertEqual(10, week_end_days)

    def test_working_delta(self):
        start_date = datetime.date(2016, 1, 1)
        end_date = ACPHoliday.working_delta(start_date, 15)
        self.assertEqual(datetime.date(2016, 1, 25), end_date)

        end_date = ACPHoliday.working_delta(start_date, 5)
        self.assertEqual(datetime.date(2016, 1, 11), end_date)

    def test_get_working_days_for_month(self):
        working_days = ACPHoliday.get_working_days_for_month(2016, 3)
        self.assertEqual(22, working_days)

    def test_get_working_days_for_month_illegal_month(self):
        try:
            working_days = ACPHoliday.get_working_days_for_month(2016, 13)
            self.assertEqual(22, working_days)
            self.fail('IllegalMonthError was not thrown')
        except ACPCalendarException as e:
            self.assertEqual('bad month number 13; must be 1-12', str(e))

    def test_convert_to_date(self):
        study_date = ACPHoliday.convert_to_date('2016-07-08')
        self.assertEqual(datetime.date(2016, 7, 8), study_date)

    def test_convert_to_date_invalid(self):
        try:
            study_date = ACPHoliday.convert_to_date(5)
            self.fail('should throw error for dates must be either string or date objects')
        except ACPCalendarException as e:
            self.assertEqual('Dates must be either string or date objects', str(e))

    @override_settings(DEBUG=True)
    def test_write_json(self):
        dated_filename = self.get_dated_output_filename('test_write_json.json')
        results = ACPHoliday.objects.all().write_json(dated_filename)
        self.assertEqual(144, results.count())
        self.assertTrue(os.path.exists(dated_filename))

        holidays_in_json = get_holidays_list(dated_filename)
        self.assertEqual('2006-01-01', holidays_in_json[0]['date'])
        self.assertEqual('2018-12-25', holidays_in_json[-1]['date'])
        self.assertEqual(144, len(holidays_in_json))
        #self.clean_output = False
        self.clean_output_folder(dated_filename)

    @override_settings(DEBUG=True)
    def test_write_json_filter(self):
        dated_filename = self.get_dated_output_filename('test_write_json_filter.json')
        ACPHoliday.objects.update_fiscal_years()
        results = ACPHoliday.objects.filter(fiscal_year=2015).write_json(dated_filename)
        self.assertEqual(11, results.count())
        self.assertTrue(os.path.exists(dated_filename))

        holidays_in_json = get_holidays_list(dated_filename)
        self.assertEqual('2014-11-03', holidays_in_json[0]['date'])
        self.assertEqual('2015-05-01', holidays_in_json[-1]['date'])
        self.assertEqual(11, len(holidays_in_json))
        self.clean_output_folder(dated_filename)

    # def test_filter(self):
    #     results = ACPHoliday.objects.filter(fiscal_year=2015)
    #     self.assertEqual(5, results.count())
