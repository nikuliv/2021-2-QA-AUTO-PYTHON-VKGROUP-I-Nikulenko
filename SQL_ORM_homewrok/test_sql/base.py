import pytest

from mysql.client import MySQLClient
from utils.builder import MySQLBuilder


class BaseMySQL:

    def prepare(self, log_path):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, log_path):
        self.client: MySQLClient = mysql_client
        self.builder: MySQLBuilder = MySQLBuilder(self.client)

        self.prepare(log_path)
