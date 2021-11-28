import os
import socket
import json

RECONNECT_LIMIT = 5


class SocketClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'requests.log'))

        # recreating log file
        log = open(self.log_file, 'w')
        log.close()

    def _connect(self):
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect.settimeout(0.1)

        for i in range(RECONNECT_LIMIT):
            try:
                connect.connect((self.host, self.port))
                return connect
            except ConnectionRefusedError:
                if i == RECONNECT_LIMIT - 1:
                    print("\n\nConcetcion error\n\n")
                    raise

    def log_response(self, data):
        status_code = data[0].split(' ')[1]
        headers = data[1:-2]
        body = data[-1]
        with open(self.log_file, 'a') as log:
            log.write('STATUS_CODE:\n\t' + status_code + '\n')
            log.write('HEADERS:\n')
            for header in headers:
                log.write('\t' + header + '\n')
            log.write('RESPONSE_BODY:\n\t' + body + '\n\n')

    def handle_response(self, connect):
        total_data = []
        while True:
            data = connect.recv(1024)
            if data:
                total_data.append(data.decode())
            else:
                connect.close()
                break

        data = ''.join(total_data).splitlines()
        self.log_response(data)

        return {'status_code': int(data[0].split(' ')[1]), 'body': data[-1]}

    @staticmethod
    def to_json(dictionary):
        return json.dumps(dictionary, indent=4)

    def get(self, url):
        connect_get = self._connect()

        request = f'GET {url} HTTP/1.1\r\n' \
                  f'Host:{self.host}\r\n\r\n'

        for i in range(RECONNECT_LIMIT):
            try:
                connect_get.send(request.encode())
                return self.handle_response(connect_get)
            except BrokenPipeError:
                if i == RECONNECT_LIMIT - 1:
                    raise

    def post(self, url, data):
        connect_post = self._connect()
        json_data = self.to_json(data)

        content_type = 'Content-Type: application/json'
        content_length = 'Content-Length: ' + str(len(json_data))
        request = f'POST {url} HTTP/1.1\r\n' \
                  f'Host: {self.host}\r\n' \
                  f'{content_type}\r\n' \
                  f'{content_length}\r\n\r\n' \
                  + json_data

        connect_post.send(request.encode())

        return self.handle_response(connect_post)

    def put(self, url, data):
        connect_put = self._connect()
        json_data = self.to_json(data)

        content_type = 'Content-Type: application/json'
        content_length = 'Content-Length:' + str(len(json_data))
        request = f'PUT {url} HTTP/1.1\r\n' \
                  f'Host:{self.host}\r\n' \
                  f'{content_type}\r\n' \
                  f'{content_length}\r\n\r\n' \
                  + json_data

        connect_put.send(request.encode())

        return self.handle_response(connect_put)

    def delete(self, url, data):
        connect_delete = self._connect()
        json_data = self.to_json(data)

        content_type = 'Content-Type: application/json'
        content_length = 'Content-Length:' + str(len(json_data))
        request = f'DELETE {url} HTTP/1.1\r\n' \
                  f'Host: {self.host}\r\n' \
                  f'{content_type}\r\n' \
                  f'{content_length}\r\n\r\n' \
                  + json_data

        connect_delete.send(request.encode())

        return self.handle_response(connect_delete)