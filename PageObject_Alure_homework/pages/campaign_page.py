import os
import logging
import allure
from faker import Faker
from selenium.webdriver import ActionChains

from constants import *
from pages.base_page import BasePage
from ui.locators.locators import CampaignPageLocators

logger = logging.getLogger('test')


class CampaignPage(BasePage):
    locators = CampaignPageLocators()
    fake = Faker()

    @allure.step('Loading a banner for an advertising campaign')
    def upload(self, locator):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'images', 'campaign.jpg'))
        upload_field = self.find(locator)
        upload_field.send_keys(file_path)

    def go_to_creation_campaign(self):
        return self.driver.get('https://target.my.com/campaign/new')

    def create_campaign_name(self):
        return self.fake.bothify(text='campaign-???-#########-???-###')

    def set_date(self, start_date, end_date):
        from_date = self.find(start_date)
        from_date.send_keys(DATE_FROM)
        to_date = self.find(end_date)
        to_date.send_keys(DATE_TO)

    def set_cost(self, per_day, total):
        day_budget = self.find(per_day)
        day_budget.send_keys(BUDGET_PER_DAY)
        total_budget = self.find(total)
        total_budget.send_keys(BUDGET_PER_DAY)

    @allure.step('Creation of an advertising campaign')
    def create_campaign(self):
        name = self.create_campaign_name()
        self.go_to_creation_campaign()
        self.click(self.locators.COVERAGE_LOCATOR)
        self.send_message(self.locators.LINK_INPUT_LOCATOR, 'https://github.com/nikuliv')
        self.send_message(self.locators.CAMPAIGN_NAME_LOCATOR, name)
        self.click(self.locators.BANNER_IMAGE_LOCATOR)
        self.upload(self.locators.UPLOAD_LOCATOR)
        self.set_date(self.locators.DATE_FROM_LOCATOR, self.locators.DATE_TO_LOCATOR)
        self.set_cost(self.locators.BUDGET_DAY, self.locators.BUDGET_TOTAL)
        self.click(self.locators.CREATE_CAMPAIGN_LOCATOR)
        logger.info(f'Advertising campaign {name} has been created')

        return name