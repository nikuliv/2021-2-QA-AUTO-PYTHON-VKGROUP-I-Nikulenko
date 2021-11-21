import os
from collections import Counter
from fnmatch import fnmatch
from urllib.parse import quote_plus

LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, './access.log'))


def count_requests():
    with open(LOG, 'r') as log:
        all_requests_count = len(log.readlines())
    return all_requests_count


def count_request_types():
    with open(LOG, 'r') as log:
        req_type_column = [req.split()[5][1:] for req in log.readlines()]
        req_types = Counter(req_type_column).most_common()
    return req_types


def most_frequent_requests():
    with open(LOG, 'r') as log:
        url_column = [quote_plus(req.split()[6]) for req in log.readlines()]
        freq_requests = Counter(url_column).most_common(10)

    return freq_requests


def largest_4xx_requests():
    with open(LOG, 'r') as log:
        url_code_size_ip_columns = [(quote_plus(req.split()[6]), int(req.split()[8]), int(req.split()[9]), req.split()[0])
                                    for req in log.readlines() if fnmatch(req.split()[8], '4??')]
        url_code_size_ip_columns.sort(key=lambda req: req[2], reverse=True)

    return url_code_size_ip_columns[:5]


def users_with_5xx_requests():
    with open(LOG, 'r') as log:
        ip_with_5xx = [req.split()[0] for req in log.readlines() if fnmatch(req.split()[8], '5??')]
        freq_ip = Counter(ip_with_5xx).most_common(5)

    return freq_ip
