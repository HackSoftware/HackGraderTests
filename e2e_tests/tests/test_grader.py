import requests
import json
import time
from urllib.parse import urlparse

from test_plus import TestCase

from django.conf import settings
from ..helpers import read_binary_file, output_checking_test_binary, get_headers


class HackTesterValidSolutionTests(TestCase):
    def test_get_on_index_is_successful(self):
        response = requests.get('http://localhost:8000')
        self.response_200(response)

    def test_get_on_grade_without_headers_is_not_successful(self):
        response = requests.get(settings.GRADE_URL)
        self.response_400(response)

    def test_posting_with_valid_python_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('e2e_tests/fixtures/binary/solution.py'),
            "test": read_binary_file('e2e_tests/fixtures/binary/tests.py'),
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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

    def test_posting_with_valid_ruby_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file('e2e_tests/fixtures/binary/solution.rb'),
            "test": read_binary_file('e2e_tests/fixtures/binary/tests.rb'),
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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

    def test_posting_with_valid_java_solution_and_tests_is_successful(self):
        data = {
            'test_type': 'unittest',
            'language': 'java',
            'solution': read_binary_file('e2e_tests/fixtures/binary/solution.jar'),
            'test': read_binary_file('e2e_tests/fixtures/binary/tests.jar'),
            'extra_options': {
                'qualified_class_name': 'com.hackbulgaria.grader.Tests'
            }
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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

    def test_posting_with_valid_js_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "javascript/nodejs",
            "solution": read_binary_file('e2e_tests/fixtures/binary/solution.js'),
            "test": read_binary_file('e2e_tests/fixtures/binary/tests.js'),
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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

    def test_posting_with_valid_django_binary_solution_and_tests_archive_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('e2e_tests/fixtures/binary/django/4/solution.py'),
            "test": read_binary_file('e2e_tests/fixtures/binary/django/4/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'lint': False,
                'time_limit': 20
            }
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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

    def test_posting_with_valid_django_archive_solution_and_archive_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('e2e_tests/fixtures/binary/django/2/django_project.tar.gz'),
            "test": read_binary_file('e2e_tests/fixtures/binary/django/2/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'archive_solution_type': True,
                'lint': False,
                'time_limit': 30
            }
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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


class HackTesterErrorTests(TestCase):
    def test_posting_python_solution_with_flake8_error_and_lint_true_is_invalid(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file('e2e_tests/fixtures/binary/solution_flake8_error.py'),
            "test": read_binary_file('e2e_tests/fixtures/binary/tests.py'),
            "extra_options": {
                "lint": True
            }
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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
        self.assertEqual('lint_error', response_text['output']['test_status'])

    def test_posting_ruby_solution_with_rubocop_error_is_invalid(self):
        data = {
            "test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file('e2e_tests/fixtures/binary/solution_rubocop_error.rb'),
            "test": read_binary_file('e2e_tests/fixtures/binary/tests.rb'),
            "extra_options": {
                "lint": True
            }
        }

        req_and_resource = "POST {}".format(settings.GRADE_PATH)
        headers = get_headers(json.dumps(data), req_and_resource)
        response = requests.post(settings.GRADE_URL, json=data, headers=headers)
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
        self.assertEqual('lint_error', response_text['output']['test_status'])
