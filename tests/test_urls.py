from django.conf.urls import url, include
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

urlpatterns = [
    url(r'^calendar/', include('acp_calendar.urls', namespace='calendar')),
]

@override_settings(ROOT_URLCONF=__name__)
class TestUrls(TestCase):

    def test_working_days_url(self):
        result = {"start_date": "2016-01-01", "end_date": "2016-01-31"}
        url = reverse('calendar:calendar-api:working_days', kwargs=result)
        self.assertEqual('/calendar/api/working-days/2016-01-01/2016-01-31/', url)

    def test_fiscal_year_calendar(self):
        url = reverse('calendar:fiscal-year-calendar', kwargs={'fiscal_year': 2017})
        self.assertEqual('/calendar/fiscal-year-calendar/2017', url)
