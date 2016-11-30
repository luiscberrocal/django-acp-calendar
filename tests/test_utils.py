from django.test import TestCase

from acp_calendar.utils import compare_initial_data_against_db


class TestUtils(TestCase):

    def test_compare_initial_data_against_db(self):
        not_found = compare_initial_data_against_db()
        self.assertEqual(0, len(not_found))
