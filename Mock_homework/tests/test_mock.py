import pytest
import json
from mock.flask_mock import app_data
from utils.data_gen import create_user_name, create_user_phone_number
from base import MockBase


class TestPostRequests(MockBase):

    def test_create_user(self, connect):
        test_user, resp = self.create_user(connect)
        assert resp['status_code'] == 201

        body = json.loads(resp['body'])
        assert body['name'] == test_user['name']
        assert body['phone_number'] == test_user['phone_number']

    def test_create_existent_user(self, connect):
        # create
        test_user, resp = self.create_user(connect)
        assert resp['status_code'] == 201
        # recreate
        resp = connect.post('/create_user', test_user)
        assert resp['status_code'] == 400


class TestGetRequests(MockBase):

    def test_get_phone_number(self, connect):
        # create
        test_user, resp = self.create_user(connect)
        assert resp['status_code'] == 201
        # get number
        user_name = test_user.get('name')
        resp = connect.get(f'/get_phone/' + user_name)
        assert resp['status_code'] == 200

        body = json.loads(resp['body'])
        assert body['phone_number'] == app_data[user_name]

    def test_get_phone_number_of_non_existent_user(self, connect):
        non_existent_username = create_user_name() + 'non-existent'
        resp = connect.get(f'/get_phone/' + non_existent_username)
        assert resp['status_code'] == 404


class TestDeleteRequests(MockBase):

    def test_delete_user(self, connect):
        # create
        test_user, resp = self.create_user(connect)
        assert resp['status_code'] == 201
        # delete
        resp = connect.delete('/delete_user', test_user)
        assert resp['status_code'] == 200

    def test_delete_non_existent_user(self, connect):
        user_name = create_user_name()
        non_existent_user = {'name': 'new' + user_name}
        resp = connect.delete('/delete_user', non_existent_user)
        assert resp['status_code'] == 404


class TestPutRequests(MockBase):

    def test_change_phone_number(self, connect):
        # create
        test_user, resp = self.create_user(connect)
        assert resp['status_code'] == 201
        # change number
        test_user['new_phone'] = create_user_phone_number()
        resp = connect.put('/change_phone', test_user)
        assert resp['status_code'] == 201

        body = json.loads(resp['body'])
        assert body['phone_number'] == test_user['new_phone']

    def test_change_phone_number_of_non_existent_user(self, connect):
        test_user = {'name': create_user_name() + create_user_name(), 'phone_number': create_user_phone_number(),
                     'new_phone': create_user_phone_number()}
        resp = connect.put('/change_phone', test_user)
        assert resp['status_code'] == 404
