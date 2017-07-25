import base64
import tarfile
import json
import os
import time
import hmac
import hashlib
from datetime import datetime, timedelta

from settings.local import GRADER_API_KEY, GRADER_SECRET_KEY
from settings.base import BASE_DIR


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def read_binary_file(path):
    """Returns the file in base64 encoding"""

    with open(path, 'rb') as f:
        encoded = base64.b64encode(f.read())

    return encoded.decode('ascii')


def create_tar_gz_archive(language):
    path_to_tests = os.path.join(BASE_DIR + "fixtures", "output_check", language, "tests")
    test_files = os.listdir(path_to_tests)
    with tarfile.open(name="archive.tar.gz", mode="w:gz") as tar:
        for file in test_files:
            path_to_file = os.path.join(path_to_tests, file)
            tar.add(path_to_file, arcname=file)

    return tar.name


def output_checking_test_binary(language):
    test_archive = create_tar_gz_archive(language)
    binary = read_binary_file(test_archive)
    os.remove(test_archive)

    return binary


def get_and_update_nonce(resource):
    data = {}
    r = -1

    with open('nonce.json', 'r') as f:
        data = json.load(f)

    if resource not in data:
        r = 1
        data[resource] = [r]
    else:
        r = max(data[resource]) + 1
        data[resource].append(r)

    with open('nonce.json', 'w') as f:
        json.dump(data, f, indent=4)

    return str(r)


def get_headers(body, req_and_resource):
    nonce = get_and_update_nonce(req_and_resource)
    date = time.strftime("%c")
    msg = body + date + nonce
    digest = hmac.new(bytearray(GRADER_SECRET_KEY.encode('utf-8')),
                      msg=msg.encode('utf-8'),
                      digestmod=hashlib.sha256).hexdigest()

    request_headers = {'Authentication': digest,
                       'Date': date,
                       'X-API-Key': GRADER_API_KEY,
                       'X-Nonce-Number': nonce}

    return request_headers


def elapsed_time(time):
    cur_time = datetime.now()
    return (cur_time - time).seconds
