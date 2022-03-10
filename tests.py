import unittest
from getcountries import alert_country
from main import request_country



class TestCountry(unittest.TestCase):
    def test_for_type_list(self):
        self.assertEqual(type(request_country()), list)
