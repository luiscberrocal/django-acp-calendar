from django.core.urlresolvers import reverse
from django.test import TestCase


class TestUrls(TestCase):

    def test_working_days_url(self):
        result = {"start_date": "2016-01-01", "end_date": "2016-01-31"}
        url = reverse('calendar-api:working_days', kwargs=result)
        self.assertEqual('/api/working-days/2016-01-01/2016-01-31/', url)
