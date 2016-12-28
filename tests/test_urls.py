from django.core.urlresolvers import reverse
from django.test import TestCase


class TestUrls(TestCase):

    def test_working_days_url(self):
        result = {"start_date": "2016-01-01", "end_date": "2016-01-31"}
        url = reverse('calendar-api:working_days', kwargs=result)
        self.assertEqual('/api/working-days/2016-01-01/2016-01-31/', url)

    def test_fiscal_year_calendar(self):
        url = reverse('fiscal-year-calendar', kwargs={'fiscal_year': 2017})
        self.assertEqual('/fiscal-year-calendar/2017', url)
