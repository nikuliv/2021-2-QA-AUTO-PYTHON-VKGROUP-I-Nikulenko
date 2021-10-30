import pytest
from _pytest.fixtures import FixtureRequest

from pages.base_page import BasePage
from pages.unauthorized_page import UnauthorizedPage
from pages.authorized_page import AuthorizedPage
from pages.campaign_page import CampaignPage
from pages.segment_page import SegmentPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.unauthorized_page: UnauthorizedPage = request.getfixturevalue('unauthorized_page')
        self.authorized_page: AuthorizedPage = request.getfixturevalue('authorized_page')
        self.campaign_page: CampaignPage = request.getfixturevalue('campaign_page')
        self.segment_page: SegmentPage = request.getfixturevalue('segment_page')

        self.logger.info('Первоначальная настройка завершена!')