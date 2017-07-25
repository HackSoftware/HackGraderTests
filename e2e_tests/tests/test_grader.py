import requests
import json
import time
from urllib.parse import urlparse

from test_plus import TestCase

from ..client import get_headers, GRADE_PATH, GRADE_URL
from ..helpers import read_binary_file, output_checking_test_binary


class HackTesterTests(TestCase):
    def test_get_on_index_is_successful(self):
        response = requests.get('http://localhost:8000')
        self.assertEqual(200, response.status_code)

    def test_posting_with_valid_python_solution_and_tests_is_successful(self):
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

        check_url = response.headers['Location']

        path = urlparse(check_url).path
        req_and_resource = "GET {}".format(path)
        headers = get_headers(path, req_and_resource)
        response = requests.get(check_url, headers=headers)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            headers = get_headers(path, req_and_resource)
            response = requests.get(check_url, headers=headers)
            time.sleep(1)

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])
