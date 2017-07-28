import requests
import json
from datetime import datetime

from unittest import TestCase

from settings.base import GRADE_URL, BASE_DIR, THRESHOLD
from ..helper_tests import prepare_and_get, prepare_and_post, poll
from ..helpers import read_binary_file, output_checking_test_binary, elapsed_time


class HackTesterValidSolutionTests(TestCase):
    def setUp(self):
        self.start = datetime.now()

    def test_get_on_index_is_successful(self):
        response = requests.get('http://localhost:8000')
        self.assertEqual(200, response.status_code)

    def test_get_on_grade_without_headers_is_not_successful(self):
        response = requests.get(GRADE_URL)
        self.assertEqual(400, response.status_code)

    def test_posting_with_valid_python_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.py'),
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_python_solution_with_flake8_error_and_lint_false_is_valid(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution_flake8_error.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.py'),
            "extra_options": {
                "lint": False
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_with_valid_ruby_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution.rb'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.rb'),
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_ruby_solution_with_rubocop_error_with_lint_false_is_valid(self):
        data = {
            "test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution_rubocop_error.rb'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.rb'),
            "extra_options": {
                "lint": False
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_with_valid_java_solution_and_tests_is_successful(self):
        data = {
            'test_type': 'unittest',
            'language': 'java',
            'solution': read_binary_file(BASE_DIR + 'fixtures/binary/solution.jar'),
            'test': read_binary_file(BASE_DIR + 'fixtures/binary/tests.jar'),
            'extra_options': {
                'qualified_class_name': 'com.hackbulgaria.grader.Tests'
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_with_valid_js_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "javascript/nodejs",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution.js'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.js'),
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_with_valid_django_solution_and_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/django/1/django_project.tar.gz'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/django/1/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'archive_solution_type': True,
                'lint': False,
                'time_limit': 120
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_with_django_solution_and_archive_tests_without_project_requirements_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/django/2/django_project.tar.gz'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/django/2/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'archive_solution_type': True,
                'lint': False,
                'time_limit': 120
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_with_django_archive_solution_and_binary_tests_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/django/3/django_project.tar.gz'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/django/3/test.py'),
            "extra_options": {
                'archive_solution_type': True,
                'lint': False,
                'time_limit': 90
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])

    def test_posting_with_django_binary_solution_and_tests_archive_is_successful(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/django/4/solution.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/django/4/tests.tar.gz'),
            "extra_options": {
                'archive_test_type': True,
                'lint': False,
                'time_limit': 90
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('OK', response_text['output']['test_status'])


class HackTesterOutputValidTests(TestCase):
    def setUp(self):
        self.start = datetime.now()

    def test_output_check_with_valid_python_binary_solution_and_test_archive_is_successful(self):
        tests = output_checking_test_binary("python")
        data = {
            "test_type": "output_checking",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/output_check/python/solution.py'),
            "test": tests,
            "extra_options": {
                'archive_test_type': True
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        for output in response_text['output']:
            self.assertEqual('OK', output['test_status'])
            self.assertEqual('ok', output['test_output'])

    def test_output_check_with_valid_ruby_binary_solution_and_test_archive_is_successful(self):
        tests = output_checking_test_binary("ruby")
        data = {
            "test_type": "output_checking",
            "language": "ruby",
            "solution": read_binary_file(BASE_DIR + 'fixtures/output_check/ruby/solution.rb'),
            "test": tests,
            "extra_options": {
                'archive_test_type': True
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        for output in response_text['output']:
            self.assertEqual('OK', output['test_status'])
            self.assertEqual('ok', output['test_output'])

    def test_output_check_with_valid_java_binary_solution_and_test_archive_is_successful(self):
        tests = output_checking_test_binary("java")
        data = {
            "test_type": "output_checking",
            "language": "java",
            "solution": read_binary_file(BASE_DIR + 'fixtures/output_check/java/solution.java'),
            "test": tests,
            "extra_options": {
                'archive_test_type': True,
                "class_name": "Factorial"
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        for output in response_text['output']:
            self.assertEqual('OK', output['test_status'])
            self.assertEqual('ok', output['test_output'])


class HackTesterErrorTests(TestCase):
    def setUp(self):
        self.start = datetime.now()

    def test_posting_python_solution_with_flake8_error_and_lint_true_is_invalid(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution_flake8_error.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.py'),
            "extra_options": {
                "lint": True
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('lint_error', response_text['output']['test_status'])

    def test_posting_ruby_solution_with_rubocop_error_with_lint_true_is_invalid(self):
        data = {
            "test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution_rubocop_error.rb'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.rb'),
            "extra_options": {
                "lint": True
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('lint_error', response_text['output']['test_status'])

    def test_fork_bomb(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/fork_bomb.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.py'),
            "extra_options": {
                "lint": True
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('test_run_error', response_text['output']['test_status'])

    def test_memory_limit(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/memory_limit.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/memory_limit_tests.py'),
            "extra_options": {
                "lint": True
            }
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('test_run_error', response_text['output']['test_status'])

    def test_js_infinite_loop_solution_with_valid_tests(self):
        data = {
            "test_type": "unittest",
            "language": "javascript/nodejs",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/infiniteLoop_solution.js'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/infiniteLoop_tests.js'),
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('time_limit_reached', response_text['output']['test_status'])

    def test_python_infinite_loop_solution_with_valid_tests(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/while_true_solution.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/while_true_tests.py'),
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('time_limit_reached', response_text['output']['test_status'])

    def test_ruby_infinite_loop_solution_with_valid_tests(self):
        data = {
            "test_type": "unittest",
            "language": "ruby",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/exec_loop_solution.rb'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/exec_loop_tests.rb'),
        }

        response = prepare_and_post(data)
        self.assertEqual(202, response.status_code)

        response, check_url, path, req_and_resource = prepare_and_get(response)

        while response.status_code != 200:
            self.assertEqual(204, response.status_code)
            response = poll(check_url, path, req_and_resource)
            time = elapsed_time(self.start)
            if time > THRESHOLD:
                break

        self.assertEqual(200, response.status_code)
        response_text = json.loads(response.text)
        self.assertEqual('time_limit_reached', response_text['output']['test_status'])
