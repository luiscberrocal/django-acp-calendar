from django.test import TestCase
from django.test import override_settings

from acp_calendar.utils import compare_initial_data_against_db
from tests.utils import build_fake_initial_data_json

test_data_filename = build_fake_initial_data_json()


class TestUtils(TestCase):


    def test_compare_initial_data_against_db(self):
        not_found = compare_initial_data_against_db()
        self.assertEqual(0, len(not_found))

    @override_settings(INITIAL_DATA_FILENAMEd=test_data_filename)
    def test_compare_initial_data_against_db2(self):
        not_found = compare_initial_data_against_db()
        self.assertEqual(0, len(not_found))
