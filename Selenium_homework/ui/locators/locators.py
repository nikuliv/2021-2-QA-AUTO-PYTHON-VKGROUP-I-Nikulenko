from selenium.webdriver.common.by import By

# BASIC LOCATORS
# LOG IN
SIGN_IN_LOCATOR = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
EMAIL_LOCATOR = (By.XPATH, "//input[@name='email']")
PASSWORD_LOCATOR = (By.XPATH, "//input[@name='password']")
ENTER_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")

# LOG OUT
USER_INFO_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
LOG_OUT_LOCATOR = (By.XPATH, "//a[@href='/logout']")

# PAGES
SEGMENTS_LOCATOR = (By.XPATH, "//a[@href='/segments']")
STATISTICS_LOCATOR = (By.XPATH, "//a[contains(@class, 'center-module-statistics')]")

# PROFILE INFO
PROFILE_LOCATOR = (By.XPATH, "//a[@href='/profile']")
FIO_LOCATOR = (By.XPATH, "//div[@data-name='fio']/div/input")
PHONE_LOCATOR = (By.XPATH, "//div[@data-name='phone']/div/input")
SAVE_LOCATOR = (By.XPATH, "//div[contains(@class, 'button') and contains(text(), 'Сохранить')]")