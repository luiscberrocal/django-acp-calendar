import json
from datetime import datetime
from unittest.mock import patch, Mock

import django
import pytz
from django.conf import settings
from django.conf.urls import url, include
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import override_settings

from acp_calendar.forms import CalculatorForm
from acp_calendar.models import ACPHoliday, FiscalYear
from acp_calendar import __version__ as version_num

urlpatterns = [url(r'^calendar/', include('acp_calendar.urls', namespace='calendar')), ]


@override_settings(ROOT_URLCONF=__name__)
class TestHomeView(TestCase):

    def test_get(self):
        url = reverse('calendar:home')
        response = self.client.get(url)
        self.assertEqual('2006-01-01', response.context['first_holiday'].date.strftime('%Y-%m-%d'))
        self.assertEqual('2017-12-25', response.context['last_holiday'].date.strftime('%Y-%m-%d'))
        self.assertEqual(133, response.context['holiday_count'])
        self.assertEqual(version_num, response.context['version'])
        self.assertEqual(0, len(response.context['years']))

    def test_post_update_fiscal_year(self):
        url = reverse('calendar:home')
        response = self.client.post(url, data={'update_fiscal_year': 'Update Fiscal Year'})
        self.assertEqual(13, len(response.context['years']))

    def test_check_initial_data(self):
        url = reverse('calendar:home')
        response = self.client.post(url, data={'check_initial_data': 'Check Initial Data'})
        self.assertEqual(0, len(response.context['not_found']))


@override_settings(ROOT_URLCONF=__name__)
class TestACPHolidayView(TestCase):

    def test_get_list(self):
        url = reverse('calendar:list')
        response = self.client.get(url)
        self.assertEqual('2006-01-01', response.context['acpholiday_list'].first().date.strftime('%Y-%m-%d'))
        self.assertEqual('2017-12-25', response.context['acpholiday_list'].last().date.strftime('%Y-%m-%d'))
        self.assertEqual(10, response.context['acpholiday_list'].count())

    def test_get_list_per_year(self):
        url = reverse('calendar:list-year', kwargs={'year': 2016})
        response = self.client.get(url)
        self.assertEqual('2016-01-01', response.context['acpholiday_list'].first().date.strftime('%Y-%m-%d'))
        self.assertEqual('2016-12-26', response.context['acpholiday_list'].last().date.strftime('%Y-%m-%d'))
        self.assertEqual(10, response.context['acpholiday_list'].count())



class TestACPHolidayListAPIView(TestCase):

    def test_get(self):
        response = self.client.get('/api/holiday-list/')
        data = json.loads(response.content.decode('utf-8'))
        results = data['results']
        self.assertEqual(20, len(results))
        self.assertEqual(133, data['count'])
        self.assertEqual('2006-01-01', results[0]['date'])

    def test_get_year(self):
        response = self.client.get('/api/holiday-list/2013/')
        data = json.loads(response.content.decode('utf-8'))
        results = data['results']
        self.assertEqual(11, len(results))
        self.assertEqual(11, data['count'])
        self.assertEqual('2013-01-01', results[0]['date'])


class TestCalendarCalculationsView(TestCase):

    def test_get(self):
        result = {"start_date": "2016-01-01", "end_date": "2016-01-31", "days": '19'}
        response = self.client.get('/api/working-days/{start_date}/{end_date}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_get_error_invalid_date(self):
        result = {"start_date": "2006-13-07", "end_date": "2006-01-31", "days": '-1',
                  'error': "time data '2006-13-07' does not match format '%Y-%m-%d'"}
        response = self.client.get('/api/working-days/{start_date}/{end_date}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_get_error_start_date(self):
        result = {"start_date": "2005-12-31", "end_date": "2006-01-31", "days": '-1',
                  'error': 'Start date precedes the first registered holiday'}
        response = self.client.get('/api/working-days/{start_date}/{end_date}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_get_error_end_date(self):
        result = {"start_date": "2017-01-07", "end_date": "2017-12-31", "days": '-1',
                  'error': 'End date exceed the last registered holiday'}
        response = self.client.get('/api/working-days/{start_date}/{end_date}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_get_error_start_greater_than_end(self):
        result = {"start_date": "2016-01-07", "end_date": "2015-12-31", "days": '-1',
                  'error': 'Start date cannot occur after end date'}
        response = self.client.get('/api/working-days/{start_date}/{end_date}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_get_working_delta(self):
        result = {"start_date": "2016-01-01", "end_date": "2016-01-11", "days": '5'}
        response = self.client.get('/api/working-delta/{start_date}/{days}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_working_month(self):
        result = {"year": "2016", "month": "3", "days": '22'}
        response = self.client.get('/api/working-month/{year}/{month}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_working_month_error(self):
        result = {"year": "2016", "month": "13", "days": '-1', 'error': 'bad month number 13; must be 1-12'}
        response = self.client.get('/api/working-month/{year}/{month}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

@override_settings(ROOT_URLCONF=__name__)
class TestCalendarView(TestCase):

    version_regex = r'\d{1,2}\.\d{1,2}\.\d{1,5}'

    @patch('django.utils.timezone.now')
    def test_get_current(self, timezone_now_date):
        time_zone = pytz.timezone(settings.TIME_ZONE)
        aware_datetime = time_zone.localize(datetime(2016, 10, 23, 20, 0), is_dst=None)
        timezone_now_date.return_value = aware_datetime

        url = reverse('calendar:fiscal-year-calendar', kwargs={'fiscal_year': 2017})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertRegex(response.context['version'], self.version_regex)
        self.assertEqual(2017, response.context['fiscal_year'])
        self.assertEqual(249, response.context['working_days_in_fiscal_year'])
        self.assertEqual(234, response.context['remaining_working_days_in_fiscal_year'])
        months = response.context['months']
        self.assertEqual(12, len(months))
        self.assertEqual('Oct', months[0]['month'])
        self.assertEqual(2016, months[0]['year'])
        self.assertEqual(21, months[0]['working_days'])

    def test_get_previous(self):
        url = reverse('calendar:fiscal-year-calendar', kwargs={'fiscal_year': 2016})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertRegex(response.context['version'], self.version_regex)
        self.assertEqual(2016, response.context['fiscal_year'])
        self.assertEqual(251, response.context['working_days_in_fiscal_year'])
        months = response.context['months']
        self.assertEqual(12, len(months))
        self.assertEqual('Oct', months[0]['month'])
        self.assertEqual(2015, months[0]['year'])
        self.assertEqual(22, months[0]['working_days'])


    def test_get_with_errors(self):
        last_holiday = ACPHoliday.objects.last()
        fiscal_year = FiscalYear.create_from_date(last_holiday.date)
        year = fiscal_year.year + 1
        url = reverse('calendar:fiscal-year-calendar', kwargs={'fiscal_year': year})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertRegex(response.context['version'], self.version_regex)
        self.assertEqual(year, response.context['fiscal_year'])
        self.assertEqual('End date exceed the last registered holiday', response.context['errors'])


@override_settings(ROOT_URLCONF=__name__)
class TestCalulatorView(TestCase):

    version_regex = r'\d{1,2}\.\d{1,2}\.\d{1,5}'

    def test_get(self):
        url = reverse('calendar:calculator')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(isinstance(response.context[-1]['form'], CalculatorForm))
        self.assertRegex(response.context['version'], self.version_regex)

    def test_post(self):
        data = {'start_date': '2016-01-01', 'end_date': '2016-02-25'}
        url = reverse('calendar:calculator')
        response = self.client.post(url, data=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(37, response.context[-1]['working_days'])
        self.assertRegex(response.context['version'], self.version_regex)

    def test_post_wrong_dates(self):
        data = {'start_date': '2016-01-01', 'end_date': '2015-02-25'}
        url = reverse('calendar:calculator')
        response = self.client.post(url, data=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(None, response.context[-1]['working_days'])
        self.assert_message_count(response, 1)
        self.assert_message_contains(response, 'Start date cannot occur after end date')
        self.assertRegex(response.context['version'], self.version_regex)

    def test_post_invalid_form(self):
        data = {'start_date': '2016-01-01', 'end_date': 'hjudas'}
        url = reverse('calendar:calculator')
        response = self.client.post(url, data=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(None, response.context[-1]['working_days'])
        self.assertRegex(response.context['version'], self.version_regex)
        self.assertEqual('Enter a valid date.', response.context['form'].errors['end_date'][0])


    def assert_message_count(self, response, expect_num):
        """
        Asserts that exactly the given number of messages have been sent.
        From: http://stackoverflow.com/questions/2897609/how-can-i-unit-test-django-messages
        """
        if django.VERSION > (1, 11):
            actual_num = len(response.context['messages'])
        else:
            actual_num = len(response.wsgi_request._messages)

        if actual_num != expect_num:
            self.fail('Message count was %d, expected %d' %
                (actual_num, expect_num))

    def assert_message_contains(self, response, text, level=None):
        """
        Asserts that there is exactly one message containing the given text.
        From: http://stackoverflow.com/questions/2897609/how-can-i-unit-test-django-messages
        """
        if django.VERSION > (1, 11):
            messages = response.context['messages']
        else:
            messages = response.wsgi_request._messages

        matches = [m for m in messages if text in m.message]

        if len(matches) == 1:
            msg = matches[0]
            if level is not None and msg.level != level:
                self.fail('There was one matching message but with different'
                    'level: %s != %s' % (msg.level, level))

            return

        elif len(matches) == 0:
            messages_str = ", ".join('"%s"' % m for m in messages)
            self.fail('No message contained text "%s", messages were: %s' %
                (text, messages_str))
        else:
            self.fail('Multiple messages contained text "%s": %s' %
                (text, ", ".join(('"%s"' % m) for m in matches)))
