import requests
import json

from test_plus import TestCase

from .client import get_headers, GRADE_PATH, GRADE_URL
from .helpers import read_binary_file, output_checking_test_binary


class HackTesterTests(TestCase):
    def test_get_on_index_is_successful(self):
        response = requests.get('http://localhost:8000')
        self.assertEqual(200, response.status_code)

    def test_posting_with_valid_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('e2e_tests/fixtures/binary/solution.py'),
            "test": read_binary_file('e2e_tests/fixtures/binary/tests.py'),
        }

        req_and_resource = "POST {}".format(GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(GRADE_URL, json=data, headers=headers)
        self.assertEqual(202, response.status_code)
