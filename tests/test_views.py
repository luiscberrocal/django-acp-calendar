import json
from django.test import TestCase


class TestViews(TestCase):

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
        result = {"start_date": "2006-01-07", "end_date": "2006-01-31", "days": '-1',
                  'error': 'Start date precedes the first registered holiday'}
        response = self.client.get('/api/working-days/{start_date}/{end_date}/'.format(**result))
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_get_error_end_date(self):
        result = {"start_date": "2016-01-07", "end_date": "2016-12-31", "days": '-1',
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
