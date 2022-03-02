import pytest
import allure
from ui.tests.base_case import BaseCase
from ui.fixtures import *


@allure.feature('Тесты на UI')
@allure.story('Тесты на авторизацию')
class TestAuthorizationPage(BaseCase):

    @pytest.mark.UI
    def test_fields_validation(self, setup):
        """
        Тест валидации полей в форме авторизации.
        Проверяет наличие атрибута required у полей.
        Ожидаемый результат: у полей присутствует валидация.
        """
        self.authorization_page.check_fields_validation()

    @pytest.mark.UI
    def test_fake_credentials(self, setup, fake_data):
        """
        Негативный тест на авторизацию.
        Проверяет реакцию приложения на валидные, но неподходящие данные.
        Ожидаемый результат: сообщение об ошибке 'Invalid username or password'.
        """
        self.authorization_page.login(username=fake_data['username'], password=fake_data['password'])
        self.authorization_page.find(self.authorization_page.locators.INVALID_ERROR_MESSAGE, 2)

    @pytest.mark.UI
    def test_invalid_username(self, setup, fake_data):
        """
        Негативный тест на авторизацию.
        Проверяет реакцию приложения на невалидные данные (слишком короткий username).
        Ожидаемый результат: сообщение об ошибке 'Incorrect username length'.
        """
        self.authorization_page.login(username=fake_data['username'][:3], password=fake_data['password'])
        self.authorization_page.find(self.authorization_page.locators.INCORRECT_ERROR_MESSAGE, 2)

    @pytest.mark.UI
    def test_valid_credentials(self, setup, fake_data, mysql_builder):
        """
        Позитивный тест на авторизацию.
        При помощи ORM пользователь добавляется в БД. Затем происходит попытка авторизации.
        Ожидаемый результат: найдена строка 'Logged as' на главной странице.
        """
        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'])
        self.authorization_page.login(username=fake_data['username'],
                                      password=fake_data['password'])
        self.main_page.find(self.main_page.locators.LOGGED_AS, 2)

    @pytest.mark.UI
    def test_block_user_authorization(self, setup, fake_data, mysql_builder):
        """
        Негативный тест на авторизацию.
        При помощи ORM пользователь добавляется в БД со значением атрибута access=0. Далее попытка авторизации.
        Ожидаемый результат: сообщение об ошибке 'Ваша учетная запись заблокирована'.
        """
        mysql_builder.add_user(username=fake_data['username'],
                               email=fake_data['email'],
                               password=fake_data['password'],
                               access=0)
        self.authorization_page.login(username=fake_data['username'], password=fake_data['password'])
        self.authorization_page.find(self.authorization_page.locators.BLOCK_MESSAGE, 2)

    @pytest.mark.UI
    def test_go_to_registration_page(self, setup):
        """
        Тест перехода со страницы авторизации на страницу регистрации.
        Проверяет наличие строки 'Registration' в исходном коде страницы.
        Ожидаемый результат: строка присутствует.
        """
        self.authorization_page.go_to_registration_page()
        assert 'Registration' in self.registration_page.driver.page_source
