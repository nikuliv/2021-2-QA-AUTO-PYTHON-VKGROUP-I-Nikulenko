import allure
from ui.pages.base_page import BasePage
from ui.locators import MainPageLocators


class MainPage(BasePage):

    locators = MainPageLocators()

    @allure.step('Переход с сайта по локатору {locator_hide} и переключение фокуса на соседнюю вкладку...')
    def go_out_from_hidden_locator(self, locator_main, locator_hide):
        self.click_on_hidden_element(locator_main, locator_hide)
        self.switch_to_second_tab()

    @allure.step('Переход с сайта по локатору {locator} и переключение фокуса на соседнюю вкладку...')
    def go_out_from_visible_locator(self, locator):
        self.click(locator)
        self.switch_to_second_tab()
