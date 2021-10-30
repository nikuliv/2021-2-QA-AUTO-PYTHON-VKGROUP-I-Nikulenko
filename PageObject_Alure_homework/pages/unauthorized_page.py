import logging
import allure
from pages.base_page import BasePage
from pages.authorized_page import AuthorizedPage
from ui.locators.locators import UnauthorizedPageLocators
from constants import LOGIN, PASSWORD

logger = logging.getLogger('test')


class UnauthorizedPage(BasePage):
    locators = UnauthorizedPageLocators()

    @allure.step('Authorization. E-mail: {email}. Password: {password}')
    def login(self, email=LOGIN, password=PASSWORD):
        self.click(self.locators.SIGN_IN_LOCATOR)
        self.send_message(self.locators.EMAIL_LOCATOR, email)
        self.send_message(self.locators.PASSWORD_LOCATOR, password)
        self.click(self.locators.ENTER_LOCATOR)

        if self.driver.current_url == 'https://target.my.com/dashboard':
            logger.info(f'Authorization (e-mail: {email} password: {password}) was successful')
            return AuthorizedPage(self.driver)
        else:
            logger.info(f'Authorization (e-mail: {email} password: {password}) failed')