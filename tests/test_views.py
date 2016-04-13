import json
from django.test import TestCase


class TestViews(TestCase):

    def test_get(self):
        response = self.client.get('/working-days/2016-01-01/2016-01-31/')
        result = {"start_date": "2016-01-01", "end_date": "2016-01-31", "days": 19}
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))

    def test_get_error(self):
        response = self.client.get('/working-days/2006-09-01/2016-01-31/')
        result = {"start_date": "2006-09-01", "end_date": "2016-01-31", "days": 2348}
        self.assertEqual(result, json.loads(response.content.decode('utf-8')))
