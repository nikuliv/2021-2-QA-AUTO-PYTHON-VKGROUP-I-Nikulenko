import pytest
from mysql.client import MySQLClient
import os


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MySQLClient(user='root', password='pass', db_name='TEST_SQL', host='127.0.0.1', port=3306)
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MySQLClient(user='root', password='pass', db_name='TEST_SQL', host='127.0.0.1', port=3306)
        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_table(table_name='requests_count')
        mysql_client.create_table(table_name='number_of_requests_by_type')
        mysql_client.create_table(table_name='most_frequent_requests')
        mysql_client.create_table(table_name='largest_4xx_requests')
        mysql_client.create_table(table_name='users_with_5xx_requests')
        mysql_client.connection.close()


def pytest_addoption(parser):
    parser.addoption("--log", action="store",
                     default=os.path.abspath(os.path.join(os.path.dirname(__file__), './access.log')),
                     help="log file path")


@pytest.fixture(scope='session')
def log_path(request):
    return request.config.getoption("--log")
