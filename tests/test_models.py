#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_acp-calendar
------------

Tests for `acp-calendar` models module.
"""

from django.test import TestCase

from acp_calendar import models
from acp_calendar.initial_data import get_holiday_type_list
from acp_calendar.models import HolidayType


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


    def tearDown(self):
        pass
