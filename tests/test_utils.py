from django.test import TestCase
from django.test import override_settings
from django.conf import settings

from acp_calendar import app_settings
from acp_calendar.utils import compare_initial_data_against_db
from tests.utils import build_fake_initial_data_json




class TestUtils(TestCase):


    def test_compare_initial_data_against_db(self):
        not_found = compare_initial_data_against_db()
        self.assertEqual(0, len(not_found))

    @override_settings(DEBUG=True)
    def test_compare_initial_data_against_db2(self):
        test_data_filename = build_fake_initial_data_json()
        not_found = compare_initial_data_against_db(test_data_filename)
        self.assertEqual(2, len(not_found))

    def test_settings_load_date_format(self):
        df = app_settings.LOAD_DATE_FORMAT
        self.assertEqual('%Y-%m-%d', df)

    @override_settings(ACP_CALENDAR_LOAD_DATE_FORMAT='%m-%d-%Y')
    def test_settings_load_date_format2(self):
        df = settings.ACP_CALENDAR_LOAD_DATE_FORMAT
        self.assertEqual('%m-%d-%Y', df)
