import base64
import os
from unittest import mock
from django.test import TestCase

import re
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from acp_calendar.models import ACPHoliday

import environ

from .utils import add_date_to_filename


class TestACPHolidayCommand(TestCase):


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


    def get_results(self, content):
        content.seek(0)
        lines = content.readlines()
        results = list()
        for line in lines:
            results.append(line.strip('\n'))
        return results
