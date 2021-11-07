import os
import requests
import logging
from urllib.parse import urljoin
from faker import Faker

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 500


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:
    fake = Faker()

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
        response = self.session.request(method, url, headers=headers, data=data, json=json, files=files)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')
        return response

    def _get_csrf_token(self):
        location = '/csrf/'
        self._request('GET', location)
        return self.session.cookies['csrftoken']

    def post_login(self):
        location = 'https://auth-ac.my.com/auth'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }

        data = {
            'email': self.email,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        result = self._request('POST', location, headers=headers, data=data)
        self.csrf_token = self._get_csrf_token()

        return result

    def _get_banner_id(self):
        location = '/api/v2/campaign_objective/reach/urls.json?_=1619802478801'
        response = self._request('GET', location)

        return response.json()['items'][0]['id']

    def _post_upload_image(self):
        location = '/api/v2/content/static.json'
        file_name = 'campaign.jpg'
        file_path = os.path.abspath(os.path.join('img', file_name))
        file_path = file_path.encode('utf-8')

        headers = {
            'X-CSRFToken': self._get_csrf_token()
        }

        files = {
            'file': (file_name, open(file_path, 'rb'))
        }

        response = self._request('POST', location, headers=headers, files=files)

        return response.json()['id']

    def post_campaign_create(self, name='test_campaign'):
        location = '/api/v2/campaigns.json'

        headers = {
            'X-CSRFToken': self._get_csrf_token()
        }

        data = {
            'name': name,
            'objective': 'reach',
            'package_id': 960,
            'banners': [{
                'urls': {
                    'primary': {
                        'id': self._get_banner_id()
                    }
                },
                'textblocks': {},
                'content': {
                    'image_240x400': {
                        'id': self._post_upload_image()
                    }
                },
                'name': ''}
            ]
        }

        response = self._request('POST', location, headers=headers, json=data)
        return response.json()['id']

    def get_campaign(self, campaign_id):
        location = f'/api/v2/campaigns/{campaign_id}.json'
        self._request('GET', location)

    def post_campaign_delete(self, campaign_id):
        location = f'/api/v2/campaigns/{campaign_id}.json'

        headers = {
            'X-CSRFToken': self._get_csrf_token()
        }

        data = {
            'status': 'deleted'
        }

        self._request('POST', location, headers=headers, json=data, expected_status=204)

    def create_segment_name(self):
        return self.fake.bothify(text='segment-???-#########-???-###')

    def post_segment_create(self, name='test_segment'):
        location = 'api/v2/remarketing/segments.json?fields=relations__object_type,' \
                   'relations__object_id,relations__params,relations_count,id,name,' \
                   'pass_condition,created,campaign_ids,users,flags'

        headers = {
            'X-CSRFToken': self._get_csrf_token()
        }

        data = {
            "logicType": "or",
            "name": name,
            "pass_condition": 1,
            "relations": [{
                "object_type": "remarketing_player",
                "params": {
                    "type": "positive",
                    "left": 365,
                    "right": 0
                }
            }]
        }

        response = self._request('POST', location, headers=headers, json=data)

        return response.json()['id']

    def get_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}' \
                   f'/relations.json?fields=id,params,object_type,object_id&_=1618703524358'

        self._request('GET', location)

    def delete_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}.json'

        headers = {
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self._get_csrf_token()
        }

        self._request('DELETE', location, headers=headers, expected_status=204)
