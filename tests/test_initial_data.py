from django.test import TestCase

from acp_calendar.initial_data import get_holidays_list


class TestInitialData(TestCase):

    def test_get_holidays_list(self):
        holidays = get_holidays_list()
        self.assertEqual(144, len(holidays))
        self.assertEqual('2006-01-01', holidays[0]['date'])
        self.assertEqual('2018-12-25', holidays[-1]['date'])
