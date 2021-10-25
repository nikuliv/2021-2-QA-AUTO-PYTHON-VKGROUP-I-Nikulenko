import pytest
from selenium import webdriver


@pytest.fixture(scope='class')
def driver():
    chrome = webdriver.Chrome(executable_path='C:/Users/Ilia/chromedriver/chromedriver')
    chrome.implicitly_wait(5)  # Wait implicitly for elements to be ready before attempting interactions
    chrome.get('https://target.my.com/')
    chrome.maximize_window()
    yield chrome
    chrome.quit()
