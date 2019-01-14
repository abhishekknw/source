import unittest
from unittest import TestCase
from unittest import mock
from v0.ui.analytics.views import GetLeadsDataGeneric, get_data_analytics


class TestAnalytics(TestCase):
    @mock.patch('get_data_analytics', return_value = {})
    def test_analytics_results(self,get_data_analytics):
        self.assertEqual(get_data_analytics([],[],[],[],[]), {})