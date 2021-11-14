import logging
import allure
from faker import Faker
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from ui.locators.locators import SegmentPageLocators

logger = logging.getLogger('test')


class SegmentPage(BasePage):
    locators = SegmentPageLocators()
    fake = Faker()

    def go_to_creation_segment(self):
        return self.driver.get('https://target.my.com/segments/segments_list/new')

    def create_segment_name(self):
        return self.fake.bothify(text='segment-???-#########-???-###')

    @allure.step('Segment creation {name}')
    def create_segment(self, name):
        self.go_to_creation_segment()
        self.click(self.locators.SOCIAL_NETWORK_APPLICATIONS_LOCATOR)
        self.click(self.locators.CHECKBOX_LOCATOR)
        self.click(self.locators.ADD_SEGMENT_LOCATOR)
        self.send_message(self.locators.SEGMENT_NAME_LOCATOR, name)
        self.click(self.locators.CREATE_SEGMENT_LOCATOR)
        logger.info(f'The segment {name} has been successfully created')

    @allure.step('Deleting segment {name}')
    def delete_segment(self, name):
        self.send_message(self.locators.SEARCH_SEGMENT_LOCATOR, name)
        self.click((By.XPATH, self.locators.CHOOSE_SEGMENT_LOCATOR.format(name)))
        self.click(self.locators.SEGMENT_ID_LOCATOR)
        self.click(self.locators.SEGMENT_ACTIONS_LOCATOR)
        self.click(self.locators.DELETE_SEGMENT_LOCATOR)
        self.driver.refresh()
        logger.info(f'The segment {name} has been successfully deleted')