import time
import constants
from base import BaseCase
from ui.locators import locators
import pytest


class TestLogin(BaseCase):

    @pytest.mark.UI("UI")
    def test_login(self):
        self.login(constants.LOGIN, constants.PASSWORD)
        assert self.find(locators.COMPANIES_LOCATOR)


class TestLogout(BaseCase):
    @pytest.mark.UI
    def test_logout(self):
        self.login(constants.LOGIN, constants.PASSWORD)
        self.logout()

        assert self.find(locators.SIGN_IN_LOCATOR)


class TestProfileEdit(BaseCase):
    @pytest.mark.UI
    def test_edit_profile(self):
        self.login(constants.LOGIN, constants.PASSWORD)
        fio = constants.FIO
        phone = constants.PHONE_NUMBER
        self.click(locators.PROFILE_LOCATOR)

        fio_field = self.find(locators.FIO_LOCATOR)
        fio_field.clear()
        fio_field.send_keys(fio)

        phone_field = self.find(locators.PHONE_LOCATOR)
        phone_field.clear()
        phone_field.send_keys(phone)

        self.click(locators.SAVE_LOCATOR)

        self.driver.refresh()

        assert fio == self.find(locators.FIO_LOCATOR).get_attribute('value')
        assert phone == self.find(locators.PHONE_LOCATOR).get_attribute('value')


class TestMovingBetweenPages(BaseCase):

    @pytest.mark.parametrize('locator, page_el_locator', [
        pytest.param(
            locators.SEGMENTS_LOCATOR, locators.SEGMENTS_ALIKE_LOCATOR,
            id='segments',
        ),
        pytest.param(
            locators.STATISTICS_LOCATOR, locators.STATISTICS_DOOH_LOCATOR,
            id='statistics',
        ),
    ])
    @pytest.mark.UI
    def test_transition_to_pages(self, locator, page_el_locator):
        self.login(constants.LOGIN, constants.PASSWORD)
        self.click(locator)
        time.sleep(1)
        assert self.find(page_el_locator)
        self.logout()


