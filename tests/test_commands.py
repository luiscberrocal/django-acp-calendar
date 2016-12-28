import os
from io import StringIO

import environ
from django.core.management import call_command
from django.test import TestCase
from django.test import override_settings

from acp_calendar.initial_data import get_holidays_list
from acp_calendar.models import ACPHoliday, HolidayType
from .utils import add_date_to_filename


class TestACPHolidayCommand(TestCase):

    clean_output = True


    def test_list_initial(self):
        content = StringIO()
        call_command('acp_holidays', list_initial=True, stdout=content)
        results = self.get_results(content)
        self.assertEqual(171, len(results))
        self.assertEqual('Found 133 in database', results[-1:][0])
        self.assertEqual('Found 133 in initials', results[-2:-1][0])
        self.assertEqual('\t[*] mártires                       2006-01-09', results[3:4][0])

    def test_list_initials_no_holidays(self):
        ACPHoliday.objects.all().delete()
        content = StringIO()
        call_command('acp_holidays', list_initial=True, stdout=content)
        results = self.get_results(content)
        self.assertEqual(171, len(results))
        self.assertEqual('Found 0 in database', results[-1:][0])
        self.assertEqual('Found 133 in initials', results[-2:-1][0])
        self.assertEqual('\t[-] mártires                       2006-01-09', results[3:4][0])

    @override_settings(DEBUG=True)
    def test_export_holidays(self):
        content = StringIO()
        root_dir = environ.Path(__file__) - 2
        output_dir = str(root_dir.path('output'))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filename = os.path.join(output_dir, 'holidays.json')
        dated_filename = add_date_to_filename(filename)
        call_command('acp_holidays', export_filename=dated_filename, stdout=content)
        self.assertTrue(os.path.exists(dated_filename))
        results = self.get_results(content)
        expected = 'Wrote {} holidays to {}'.format(133, dated_filename)
        self.assertEqual(expected, results[0])

        holidays_in_json = get_holidays_list(dated_filename)
        self.assertEqual('2006-01-01', holidays_in_json[0]['date'])
        self.assertEqual('2017-12-25', holidays_in_json[-1]['date'])
        if self.clean_output:
            os.remove(dated_filename)
            self.assertFalse(os.path.exists(dated_filename))

    def test_update_initial_test(self):
        content = StringIO()
        call_command('acp_holidays', update_initial_test=True, stdout=content)
        results = self.get_results(content)
        self.assertEqual('HolidayType test_holiday_type created.', results[3])
        self.assertEqual('HolidayType: 1 created, 0 updated, 0 skipped.', results[4])
        self.assertEqual('New ACPHoliday created: date: 2018-11-01 holiday_type: test_holiday_type', results[7])
        self.assertEqual('New ACPHoliday created: date: 2018-12-01 holiday_type: test_holiday_type', results[8])
        self.assertEqual('ACPHoliday: 2 created, 0 updated, 0 skipped.', results[9])

    def test_update_initial(self):
        content = StringIO()
        ACPHoliday.objects.all().delete()
        self.assertEqual(0, ACPHoliday.objects.count())
        call_command('acp_holidays', update_initial=True, stdout=content)
        results = self.get_results(content)
        self.assertEqual(133, ACPHoliday.objects.count())

    def test_update_initial_holiday_types(self):
        content = StringIO()
        HolidayType.objects.all().delete()
        self.assertEqual(0, HolidayType.objects.count())
        call_command('acp_holidays', update_initial=True, stdout=content)
        results = self.get_results(content)
        self.assertEqual(12, HolidayType.objects.count())



    def get_results(self, content):
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            results.append(line.strip('\n'))
        return results
