import os
from collections import Counter
from fnmatch import fnmatch

LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, './access.log'))
RES = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, './results', 'python_res.txt'))


def count_requests():
    with open(LOG, 'r') as log:
        all_requests_count = len(log.readlines())

    with open(RES, 'w') as res:
        res.writelines(['Total number of requests: ', str(all_requests_count), '\n'])


def count_request_by_type():
    with open(LOG, 'r') as log:
        req_type_column = [req.split()[5][1:] for req in log.readlines()]
        req_types = Counter(req_type_column).most_common()

    with open(RES, 'a') as res:
        res.write('\nTotal number of requests by type:\n')
        res.writelines([f'{req[1]} - {req[0]}\n' for req in req_types])


def most_frequent_requests():
    with open(LOG, 'r') as log:
        url_column = [req.split()[6] for req in log.readlines()]
        freq_requests = Counter(url_column).most_common(10)

    with open(RES, 'a') as res:
        res.write('\nTop 10 most frequent requests:\n')
        res.writelines([f'=====\nURL: {req[0]}\nRequests number: {req[1]}.\n' for req in freq_requests])
        res.write('=====\n')


def largest_4xx_requests():
    with open(LOG, 'r') as log:
        url_code_size_ip_columns = [(req.split()[6], int(req.split()[8]), int(req.split()[9]), req.split()[0])
                                    for req in log.readlines() if fnmatch(req.split()[8], '4??')]
        url_code_size_ip_columns.sort(key=lambda req: req[2], reverse=True)

    with open(RES, 'a') as res:
        res.write('\nTop 5 largest requests with (4XX) response:\n')
        res.writelines([f'=====\nURL: {req[0]}\nResponse: {req[1]}\nSize: {req[2]}\nIP: {req[3]}.\n'
                        for req in url_code_size_ip_columns[:5]])
        res.write('=====\n')


def users_with_5xx_requests():
    with open(LOG, 'r') as log:
        ip_with_5xx = [req.split()[0] for req in log.readlines() if fnmatch(req.split()[8], '5??')]
        freq_ip = Counter(ip_with_5xx).most_common(5)

    with open(RES, 'a') as res:
        res.write('\nTop 5 users by the number of requests that ended with (5XX) response:\n')
        res.writelines([f'=====\nIP: {ip[0]}\nRequests number: {ip[1]}\n' for ip in freq_ip])
        res.write('=====\n')


if __name__ == "__main__":
    count_requests()
    count_request_by_type()
    most_frequent_requests()
    largest_4xx_requests()
    users_with_5xx_requests()