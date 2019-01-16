from __future__ import absolute_import
import unittest
from django.test import TestCase
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch
from v0.ui.analytics.views import GetLeadsDataGeneric, get_data_analytics

class TestAnalytics(TestCase):
    #@mock.patch('v0.ui.analytics.views.get_data_analytics', return_value = {})
    def test_get_data_analytics(self):
        #result = get_data_analytics({},{},[],[],None)
        self.assertEqual(get_data_analytics({},{},[],[],None), [])



