import json
from datetime import datetime

from unittest import TestCase

from settings.base import BASE_DIR, THRESHOLD
from ..helper_tests import prepare_and_get, prepare_and_post, poll
from ..helpers import read_binary_file, elapsed_time


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

    def test_time_limit_when_it_is_too_small(self):
        data = {
            "test_type": "unittest",
            "language": "python",
            "solution": read_binary_file(BASE_DIR + 'fixtures/binary/solution.py'),
            "test": read_binary_file(BASE_DIR + 'fixtures/binary/tests.py'),
            "extra_options": {
                "lint": True,
                "time_limit": 1,
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
        self.assertEqual('time_limit_reached', response_text['output']['test_status'])
