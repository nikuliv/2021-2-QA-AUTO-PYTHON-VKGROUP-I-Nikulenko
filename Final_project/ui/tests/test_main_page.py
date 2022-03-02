import allure
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from ui.fixtures import *
from ui.pages.base_page import LocatorNotFoundError
from ui.tests.base_case import BaseCase


@allure.feature('Тесты на UI')
@allure.story('Тесты главной страницы')
class TestMainPage(BaseCase):

    @pytest.fixture(scope='function', autouse=True)
    def login(self, fake_data, setup, mysql_builder):
        """ Фикстура для авторизации пользователя. """

        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'])
        AuthorizationPage(self.driver).login(username=fake_data['username'], password=fake_data['password'])
        self.username = fake_data['username']

    @pytest.mark.UI
    def test_TM_version_button(self):
        """
        Тест кнопки 'TM version 0.1'.
        Тест проверяет возврат главной страницы по клику.
        Ожидаемый результат: найдена строка 'Logged as' на главной странице.
        """
        self.main_page.click(self.main_page.locators.TM_BUTTON, 2)
        self.main_page.find(self.main_page.locators.LOGGED_AS, 2)

    @pytest.mark.UI
    def test_home_button(self):
        """
        Тест кнопки 'HOME'.
        Тест проверяет возврат главной страницы по клику.
        Ожидаемый результат: найдена строка 'Logged as' на главной странице.
        """
        self.main_page.click(self.main_page.locators.TM_BUTTON, 2)
        self.main_page.find(self.main_page.locators.LOGGED_AS, 2)

    @pytest.mark.UI
    def test_python_button(self):
        """
        Тест кнопки 'Python'.
        Тест проверяет открытие сайта 'python.org' в новой вкладке по клику.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_visible_locator(self.main_page.locators.PYTHON_BUTTON)
        assert 'Welcome to Python.org' in self.driver.title

    @pytest.mark.UI
    def test_python_history_button(self):
        """
        Тест кнопки 'Python history'.
        Тест проверяет открытие ресурса в новой вкладке по клику.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.PYTHON_BUTTON,
                                                  self.main_page.locators.PYTHON_HISTORY)
        assert 'History of Python - Wikipedia' in self.driver.title

    @pytest.mark.UI
    def test_about_flask_button(self):
        """
        Тест кнопки 'About Flask'.
        Тест проверяет открытие документации Flask в новой вкладке по клику.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.PYTHON_BUTTON,
                                                  self.main_page.locators.ABOUT_FLASK)
        assert 'Welcome to Flask' in self.driver.title

    @pytest.mark.UI
    def test_download_centos_button(self):
        """
        Тест кнопки 'Download Centos7'.
        Тест проверяет открытие в новой вкладке ресурса для скачивания CentOS по клику.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.LINUX_BUTTON,
                                                  self.main_page.locators.DOWNLOAD_CENTOS)
        assert 'CentOS' in self.driver.title

    @pytest.mark.UI
    def test_news_button(self):
        """
        Тест кнопки 'News' во вкладке 'Networks'.
        Тест проверяет открытие в новой вкладке ресурса с новостями о Wireshark.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.NETWORK_BUTTON,
                                                  self.main_page.locators.WIRESHARK_NEWS)
        assert 'Wireshark · News' in self.driver.title

    @pytest.mark.UI
    def test_download_button(self):
        """
        Тест кнопки 'Download' во вкладке 'Networks'.
        Тест проверяет открытие в новой вкладке ресурса для скачивания Wireshark.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.NETWORK_BUTTON,
                                                  self.main_page.locators.DOWNLOAD_WIRESHARK)
        assert 'Wireshark · Go Deep.' in self.driver.title

    @pytest.mark.UI
    def test_examples_button(self):
        """
        Тест кнопки 'Examples' во вкладке 'Networks'.
        Тест проверяет открытие в новой вкладке ресурса о Tcpdump Examples.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_hidden_locator(self.main_page.locators.NETWORK_BUTTON,
                                                  self.main_page.locators.TCPDUMP_EXAMPLES)
        assert 'Tcpdump Examples' in self.driver.title

    @pytest.mark.UI
    def test_what_is_api_button(self):
        """
        Тест кнопки 'What is an API?'.
        Тест проверяет открытие статьи об API в новой вкладке по клику.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_visible_locator(self.main_page.locators.API_BUTTON)
        assert 'API - Wikipedia' in self.driver.title

    @pytest.mark.UI
    def test_future_of_internet_button(self):
        """
        Тест кнопки 'Future of Internet'.
        Тест проверяет открытие статьи о будущем Интернета в новой вкладке по клику.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_visible_locator(self.main_page.locators.FUTURE_OF_INTERNET)
        assert 'Future of internet' in self.driver.title

    @pytest.mark.UI
    def test_about_smtp_button(self):
        """
        Тест кнопки 'Lets talk about SMTP?'.
        Тест проверяет открытие статьи об SMTP в новой вкладке по клику.
        Ожидаемый результат: открывается новая вкладка с ресурсом, title страницы совпадает с нужным.
        """
        self.main_page.go_out_from_visible_locator(self.main_page.locators.SMTP)
        assert 'SMTP — Википедия' in self.driver.title

    @pytest.mark.UI
    def test_logout_button(self):
        """
        Тест кнопки 'Logout'.
        Тест проверяет логаут и возврат страницы авторизации по клику.
        Ожидаемый результат: наличие приветственной строки на странице авторизации.
        """
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)
        assert 'Welcome to the TEST SERVER' in self.authorization_page.driver.page_source

    @pytest.mark.UI
    def test_python_facts(self):
        """
        Тест наличия случайного факта о Python внизу страницы.
        Ожидаемый результат: факт присутствует.
        """
        self.main_page.find(self.main_page.locators.PYTHON_ZEN_QUOTE)

    @pytest.mark.UI
    def test_user_info(self):
        """
        Тест наличия информации о пользователе в правом верхнем углу страницы.
        Ожидаемый результат: строка 'Logged as <username>'
        """
        user_info = self.main_page.find(self.main_page.locators.LOGGED_AS).text
        assert user_info == f'Logged as {self.username}'

    @pytest.mark.UI
    def test_user_with_vk_id(self):
        """
        Тест получение VK ID пользователя.
        Тест добавляет пользователя в словарь mock, где ему присваивается VK ID.
        Затем происходит обновление страницы приложения и проверяется VK ID в правом верхнем углу главной страницы.
        Ожидаемый результат: VK ID присутствует.
        """
        with allure.step("Добавление VK ID пользователя для {username}..."):
            requests.post(f'http://0.0.0.0:9000/add_user/{self.username}')
        with allure.step('Получение VK ID пользователя {username}...'):
            response = requests.get(f'http://0.0.0.0:9000/vk_id/{self.username}').json()
        self.main_page.click(self.main_page.locators.HOME_BUTTON)
        self.main_page.find((By.XPATH, self.main_page.locators.VK_ID.format(response['vk_id'])))

    @pytest.mark.UI
    def test_user_without_vk_id(self):
        """
        Тест на отсутствие VK ID у пользователя.
        Тест проверяет VK ID пользователя на странице без добавления его в словарь mock.
        Ожидаемый результат: поле VK ID пустое.
        """
        try:
            self.main_page.find(self.main_page.locators.VK_ID_NONE, 2)
        except TimeoutException:
            raise LocatorNotFoundError('Поле VK ID не пустое!')

    @pytest.mark.UI
    def test_activity_fields_in_db(self, mysql_client):
        """
        Тест на значение полей active и start_active_time в БД после авторизации.
        Ожидаемый результат: поле active = 1, поле start_active_time не является None.
        """
        user = mysql_client.select_by_username(self.username)
        assert user.active == 1
        assert user.start_active_time is not None

    @pytest.mark.UI
    def test_active_field_after_logout(self, mysql_client):
        """
        Тест на значение поля active в БД после выхода пользователя.
        Ожидаемый результат: поле active = 0.
        """
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON, 10)
        user = mysql_client.select_by_username(self.username)
        assert user.active == 0

    @pytest.mark.UI
    def test_deauthorization_after_blocking(self, fake_data, mysql_client):
        """
        Тест на деавторизацию пользователя после блокировки.
        После авторизации поле access в БД меняется с 1 на 0 и происходит обновление страницы.
        Ожидаемый результат: наличие приветственной строки на странице авторизации.
        """
        mysql_client.drop_access_by_username(username=fake_data['username'])
        self.main_page.click(self.main_page.locators.HOME_BUTTON)
        assert 'Welcome to the TEST SERVER' in self.authorization_page.driver.page_source
