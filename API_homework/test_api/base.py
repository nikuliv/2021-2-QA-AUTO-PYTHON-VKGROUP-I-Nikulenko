import pytest


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, logger):
        self.api_client = api_client
        self.api_client.post_login()
        self.logger = logger

        if self.authorize:
            self.api_client.post_login()