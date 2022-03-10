import json
import unittest
import hashlib
from main import request_country, get_info_country


def sha1_jsonfile():
    file = open('data.json')
    filelanguage = json.loads(file.read())['Language']
    file.close()
    data = request_country()
    languages = {}
    count = 0
    for i in data:
        languages[str(count)] = hashlib.sha1(get_info_country(i)[2].encode()).hexdigest()
        count += 1
    return languages, filelanguage


class TestCountry(unittest.TestCase):

    def test_for_type_list_countries(self):
        self.assertEqual(type(request_country()), list)

    def test_sha1_code(self):
        self.assertDictEqual(sha1_jsonfile()[0], sha1_jsonfile()[1])
