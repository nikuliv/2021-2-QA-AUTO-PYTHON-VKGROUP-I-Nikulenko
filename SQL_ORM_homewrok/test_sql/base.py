import pytest

from mysql.client import MySQLClient
from utils.builder import MySQLBuilder


class BaseMySQL:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.client: MySQLClient = mysql_client
        self.builder: MySQLBuilder = MySQLBuilder(self.client)

        self.prepare()
