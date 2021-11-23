import os
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.base_page import BasePage
from pages.unauthorized_page import UnauthorizedPage
from pages.authorized_page import AuthorizedPage
from pages.campaign_page import CampaignPage
from pages.segment_page import SegmentPage


def get_driver(config, download_dir=None):
    browser_name = config['browser']
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = Options()
        if download_dir is not None:
            options.add_experimental_option("prefs", {"download.default_directory": download_dir})

        if selenoid:
            options.add_experimental_option("prefs", {"download.default_directory": '/home/selenium/Downloads'})
            capabilities = {
                'browserName': 'chrome',
                'version': '95.0'
            }
            if vnc:
                capabilities['version'] += '_vnc'
                capabilities['enableVNC'] = True

            browser = webdriver.Remote(selenoid, options=options,
                                       desired_capabilities=capabilities)
        else:
            manager = ChromeDriverManager(version='latest', log_level=0)
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    elif browser_name == 'firefox':
        manager = GeckoDriverManager(version='latest')
        browser = webdriver.Firefox(executable_path=manager.install())
    else:
        raise RuntimeError(f'Unsupported browser: {browser_name}')

    browser.maximize_window()
    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    with allure.step('Init browser'):
        browser = get_driver(config, download_dir=test_dir)
        browser.get(url)

    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request):
    url = config['url']
    config['browser'] = request.param

    browser = get_driver(config)
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def unauthorized_page(driver):
    return UnauthorizedPage(driver=driver)


@pytest.fixture
def authorized_page(driver):
    return AuthorizedPage(driver=driver)


@pytest.fixture
def campaign_page(driver):
    return CampaignPage(driver=driver)


@pytest.fixture
def segment_page(driver):
    return SegmentPage(driver=driver)


@pytest.fixture(scope='function')
def login(driver):
    return UnauthorizedPage(driver).login()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    """ Добавляет в отчёт скриншоты и логи браузера """
    failed_tests_count = request.session.testsfailed

    yield

    if request.session.testsfailed > failed_tests_count:

        screenshot_file = os.path.join(test_dir, 'fail.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'fail.png',
                           attachment_type=allure.attachment_type.PNG)
        browser_logfile = os.path.join(test_dir, 'browser.log')

        with open(browser_logfile, 'w') as logfile:
            for i in driver.get_log('browser'):
                logfile.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as logfile:
            allure.attach(logfile.read(), 'browser.log',
                          attachment_type=allure.attachment_type.TEXT)