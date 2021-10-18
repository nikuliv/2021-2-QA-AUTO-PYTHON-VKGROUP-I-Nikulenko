import time

from base import BaseCase
from ui.locators import locators
import pytest


class TestLogin(BaseCase):

    @pytest.mark.UI("UI")
    def test_login(self):
        self.login("tester.tim.vk@gmail.com", "P@ssword!")
        assert self.driver.current_url == 'https://target.my.com/dashboard'


class TestLogout(BaseCase):
    @pytest.mark.UI
    def test_logout(self):
        self.login("tester.tim.vk@gmail.com", "P@ssword!")
        self.logout()

        assert 'Войти' in self.driver.page_source


class TestProfileEdit(BaseCase):
    @pytest.mark.UI
    def test_edit_profile(self):
        self.login("tester.tim.vk@gmail.com", "P@ssword!")
        fio = 'Name Name Name'
        phone = '89998889889'
        self.click(locators.PROFILE_LOCATOR)

        fio_field = self.find(locators.FIO_LOCATOR)
        fio_field.clear()
        fio_field.send_keys(fio)

        phone_field = self.find(locators.PHONE_LOCATOR)
        phone_field.clear()
        phone_field.send_keys(phone)

        self.click(locators.SAVE_LOCATOR)

        self.driver.refresh()

        assert fio == self.find(locators.FIO_LOCATOR).get_attribute('value') and \
               phone == self.find(locators.PHONE_LOCATOR).get_attribute('value')


class TestMovingBetweenPages(BaseCase):

    @pytest.mark.parametrize('locator, url', [
        pytest.param(
            locators.SEGMENTS_LOCATOR, "https://target.my.com/segments/segments_list",
            id='segments',
        ),
        pytest.param(
            locators.STATISTICS_LOCATOR, "https://target.my.com/statistics/summary",
            id='statistics',
        ),
    ])
    @pytest.mark.UI
    def test_transition_to_pages(self, locator, url):
        self.login("tester.tim.vk@gmail.com", "P@ssword!")
        self.click(locator)
        time.sleep(1)
        cur_url = self.driver.current_url
        self.logout()
        assert cur_url == url


