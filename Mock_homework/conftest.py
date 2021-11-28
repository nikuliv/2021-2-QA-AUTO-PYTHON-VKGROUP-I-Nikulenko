import pytest
from mock import flask_mock
from client.client import SocketClient
import settings


@pytest.fixture(scope='session')
def connect():
    flask_mock.run_mock(host=settings.MOCK_HOST, port=settings.MOCK_PORT)
    client = SocketClient(host=settings.APP_HOST, port=settings.APP_PORT)
    yield client
    client.get('/shutdown')
