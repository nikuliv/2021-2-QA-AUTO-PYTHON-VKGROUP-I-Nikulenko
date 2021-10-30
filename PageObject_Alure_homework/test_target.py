import pytest
import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from base import BaseCase
from ui.fixtures import *
from constants import *


@allure.feature('UI Tests')
@allure.story('Negative login tests')
class TestLoginFailure(BaseCase):

    @pytest.mark.UI
    def test_wrong_credentials(self):

        self.unauthorized_page.login(email=LOGIN, password=WRONG_PASSWORD)
        error_message_title = self.unauthorized_page.find(self.unauthorized_page.locators.ERROR_LOCATOR).text
        assert error_message_title == 'Error'

    @pytest.mark.UI
    def test_invalid_email(self):
        self.unauthorized_page.login(email=INVALID_LOGIN, password=PASSWORD)
        assert self.unauthorized_page.find(self.unauthorized_page.locators.INVALID_EMAIL_LOCATOR)


@allure.feature('UI Tests')
@allure.story('Advertising campaign creation tests')
class TestCampaignCreation(BaseCase):

    @pytest.mark.UI
    def test_create_campaign(self, login):

        campaign_page = self.authorized_page.go_to_campaign_page()
        campaign_name = campaign_page.create_campaign()
        assert campaign_page.find((By.XPATH, campaign_page.locators.CAMPAIGN_IN_TABLE_LOCATOR.format(campaign_name)))


@allure.feature('UI Tests')
@allure.story('Segment tests')
class TestSegment(BaseCase):

    @pytest.mark.UI
    def test_create_segment(self, login):

        segment_page = self.authorized_page.go_to_segment_page()
        segment_name = segment_page.create_segment()
        assert segment_page.find((By.XPATH, segment_page.locators.SEGMENT_IN_TABLE_LOCATOR.format(segment_name)))

    @pytest.mark.UI
    def test_delete_segment(self, login):

        segment_page = self.authorized_page.go_to_segment_page()
        segment_name = segment_page.create_segment()
        segment_page.delete_segment(segment_name)
        with pytest.raises(TimeoutException):
            assert segment_page.find((By.XPATH, segment_page.locators.SEGMENT_IN_TABLE_LOCATOR.format(segment_name)), timeout=2)