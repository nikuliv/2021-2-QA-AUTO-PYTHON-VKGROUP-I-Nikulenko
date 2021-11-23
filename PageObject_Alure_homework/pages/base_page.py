import logging
import allure

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver

CLICK_RETRY = 3
logger = logging.getLogger('test')


class BasePage:
    locators = None

    def __init__(self, driver):
        self.driver = driver

    @allure.step('Click on the locator:{locator}')
    def click(self, locator, timeout=10):
        for i in range(CLICK_RETRY):
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                logger.info(f'{locator} clicked')
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def scroll_to(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    def wait(self, timeout=10):
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=10):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Sending message:<{message}> to locator:{locator} ')
    def send_message(self, locator, message, timeout=10):
        field = self.wait(timeout).until(EC.visibility_of_element_located(locator))
        field.clear()
        field.send_keys(message)
        logger.info(f'Message:<{message}> has been sent to the locator:<{locator}>')