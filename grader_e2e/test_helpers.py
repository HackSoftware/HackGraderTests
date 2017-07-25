import requests
import time
import json
from urllib.parse import urlparse

from settings.base import GRADE_PATH, GRADE_URL
from .helpers import get_headers


def prepare_and_post(data):
    req_and_resource = "POST {}".format(GRADE_PATH)
    headers = get_headers(json.dumps(data), req_and_resource)
    response = requests.post(GRADE_URL, json=data, headers=headers)
    return response


def prepare_and_get(response):
    check_url = response.headers['Location']
    path = urlparse(check_url).path
    req_and_resource = "GET {}".format(path)
    headers = get_headers(path, req_and_resource)
    response = requests.get(check_url, headers=headers)
    return response, check_url, path, req_and_resource


def poll(check_url, path, req_and_resource):
    headers = get_headers(path, req_and_resource)
    response = requests.get(check_url, headers=headers)
    time.sleep(1)
    return response
