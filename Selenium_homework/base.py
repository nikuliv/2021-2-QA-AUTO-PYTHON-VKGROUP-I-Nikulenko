import pytest
from ui.locators import locators
from selenium.common.exceptions import StaleElementReferenceException, \
    ElementClickInterceptedException, ElementNotInteractableException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CLICK_RETRY = 5


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def find(self, locator, timeout=0):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise
            except ElementNotInteractableException:
                if i == CLICK_RETRY - 1:
                    raise

    def login(self, email, password):
        self.click(locators.SIGN_IN_LOCATOR)

        email_field = self.find(locators.EMAIL_LOCATOR)
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.find(locators.PASSWORD_LOCATOR)
        password_field.clear()
        password_field.send_keys(password)

        self.click(locators.ENTER_LOCATOR)
        time.sleep(1)

    def logout(self):
        self.click(locators.USER_INFO_LOCATOR)
        self.click(locators.LOG_OUT_LOCATOR)
        time.sleep(1)