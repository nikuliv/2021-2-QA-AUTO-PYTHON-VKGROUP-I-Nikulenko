import os
import requests
import logging
from urllib.parse import urljoin
import json

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 700


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.csrf_token = None

    @staticmethod
    def log_pre(url, headers, data, expected_status):
        logger.info(f'Performing request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'expected status: {expected_status}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n'
                            f'{response.text[:MAX_RESPONSE_LENGTH]}'
                            )
            elif logger.level == logging.DEBUG:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: {response.text}\n\n'
                            )
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n'
                        )

    def _request(self, method, location, headers=None, data=None, json=None, files=None, expected_status=200):
        url = urljoin(self.base_url, location)
        self.log_pre(url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data, json=json, files=files)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')
        return response

    def _get_csrf_token(self):
        self._request('GET', '/csrf/')
        return self.session.cookies['csrftoken']

    def post_login(self):
        location = 'https://auth-ac.my.com/auth'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self.base_url
        }

        with open("static/login_data.json") as json_file:
            data = json.load(json_file)

        result = self._request('POST', location, headers=headers, data=data)
        self.csrf_token = self._get_csrf_token()

        return result

    def _get_banner_id(self, number):
        location = '/api/v2/campaign_objective/reach/urls.json?_=1619802478801'
        response = self._request('GET', location)

        return response.json()['items'][number]['id']

    def _post_upload_image(self):
        location = '/api/v2/content/static.json'
        file_name = 'campaign.jpg'
        file_path = os.path.abspath(os.path.join('img', file_name))
        file_path = file_path.encode('utf-8')

        headers = {
            'X-CSRFToken': self.csrf_token
        }

        files = {
            'file': (file_name, open(file_path, 'rb'))
        }

        response = self._request('POST', location, headers=headers, files=files)

        return response.json()['id']

    def post_campaign_create(self, name='test_campaign'):
        location = '/api/v2/campaigns.json'
        banner_num = 0

        headers = {
            'X-CSRFToken': self.csrf_token
        }

        with open("static/campaign_create.json") as json_file:
            data = json.load(json_file)

        data["name"] = name
        data["banners"][banner_num]["urls"]["primary"]["id"] = self._get_banner_id(banner_num)
        data["banners"][banner_num]["content"]["image_240x400"]["id"] = self._post_upload_image()

        response = self._request('POST', location, headers=headers, json=data)
        return response.json()['id']

    def get_campaign(self, campaign_id):
        location = f'/api/v2/campaigns/{campaign_id}.json'
        response = self._request('GET', location)
        return response.status_code

    def post_campaign_delete(self, campaign_id):
        location = f'/api/v2/campaigns/{campaign_id}.json'

        headers = {
            'X-CSRFToken': self.csrf_token
        }

        data = {
            'status': 'deleted'
        }

        self._request('POST', location, headers=headers, json=data, expected_status=204)

    def post_segment_create(self, name='test_segment'):
        location = 'api/v2/remarketing/segments.json?fields=id,name'

        headers = {
            'X-CSRFToken': self.csrf_token
        }

        with open("static/campaign_delete.json") as json_file:
            data = json.load(json_file)
        data["name"] = name

        response = self._request('POST', location, headers=headers, json=data)

        return response.json()['id']

    def get_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}' \
                   f'/relations.json'
        response = self._request('GET', location)

        return response.status_code

    def delete_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}.json'

        headers = {
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self.csrf_token
        }

        self._request('DELETE', location, headers=headers, expected_status=204)
