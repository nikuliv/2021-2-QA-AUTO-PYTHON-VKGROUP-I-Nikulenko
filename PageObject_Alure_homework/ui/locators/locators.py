from selenium.webdriver.common.by import By


class UnauthorizedPageLocators:
    SIGN_IN_LOCATOR = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
    EMAIL_LOCATOR = (By.XPATH, "//input[@name='email']")
    PASSWORD_LOCATOR = (By.XPATH, "//input[@name='password']")
    ENTER_LOCATOR = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")
    ERROR_LOCATOR = (By.XPATH, "//div[@class='formMsg_title']")
    INVALID_EMAIL_LOCATOR = (By.XPATH, "//div[contains(@class, 'notify-module-content')]")


class AuthorizedPageLocators:
    CAMPAIGNS_LOCATOR = (By.XPATH, "//a[@href='/dashboard']")
    SEGMENTS_LOCATOR = (By.XPATH, "//a[@href='/segments']")
    USER_INFO_LOCATOR = (By.XPATH, "//div[contains(@class, 'right-module-rightButton')]")
    LOG_OUT_LOCATOR = (By.XPATH, "//a[@href='/logout']")


class CampaignPageLocators:
    COVERAGE_LOCATOR = (By.XPATH, "//div[contains(@class, 'column-list-item') and contains(text(), 'Охват')]")
    DOOH_LOCATOR = (By.XPATH, "//div[contains(@class, 'column-list-item') and contains(@class, '_dooh')]")
    LINK_INPUT_LOCATOR = (By.XPATH, "//input[contains(@class, 'mainUrl-module-searchInput-1yPahG')]") #
    CAMPAIGN_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_campaign-name')]/div[@class='input__wrap']/input")
    BANNER_IMAGE_LOCATOR = (By.XPATH, "//div[@id='patterns_banner_4']")
    IMAGE_LOCATOR = (By.XPATH, "//div[contains(@class, 'roles-module-uploadButton-ZO1MPT')]")
    UPLOAD_LOCATOR = (By.XPATH, "//input[@data-test='image_240x400']")
    DATE_FROM_LOCATOR = (By.XPATH, "//div[contains(@class, 'date-setting__date-from')]/input[@type='text']")
    DATE_TO_LOCATOR = (By.XPATH, "//div[contains(@class, 'date-setting__date-to')]/input[@type='text']")
    BUDGET_DAY = (By.XPATH, "//input[@data-test='budget-per_day']")
    BUDGET_TOTAL = (By.XPATH, "//input[@data-test='budget-total']")
    CREATE_CAMPAIGN_LOCATOR = (By.XPATH, "//div[contains(@class, 'footer__button js-save-button-wrap')]")
    CAMPAIGN_IN_TABLE_LOCATOR = "//a[contains(@class, 'nameCell-module-campaignName') and @title='{}']"


class SegmentPageLocators:
    SOCIAL_NETWORK_APPLICATIONS_LOCATOR = (By.XPATH, "//div[@cid='view356']")
    CHECKBOX_LOCATOR = (By.XPATH, "//input[@type='checkbox']")
    ADD_SEGMENT_LOCATOR = (By.XPATH, "//div[@class='adding-segments-modal__btn-wrap js-add-button']")
    SEGMENT_NAME_LOCATOR = (By.XPATH, "//div[contains(@class, 'input_create-segment-form')]/div/input")
    CREATE_SEGMENT_LOCATOR = (By.XPATH, "//div[@class='create-segment-form__btn-wrap "
                                        "js-create-segment-button-wrap']/button")
    SEGMENT_IN_TABLE_LOCATOR = "//div[contains(@class, 'cells-module-nameCell')]/a[@title='{}']"
    SEARCH_SEGMENT_LOCATOR = (By.XPATH, "//div[@class='suggester-module-wrapper-2xHFdv']/div/input")
    CHOOSE_SEGMENT_LOCATOR = "//li[@title='{}']"
    SEGMENT_ID_LOCATOR = (By.XPATH, "//div[contains(@class, 'segmentsTable-module-idCellWrap')]/input")
    SEGMENT_ACTIONS_LOCATOR = (By.XPATH, "//div[contains(@class, 'select-module-arrow')]")
    DELETE_SEGMENT_LOCATOR = (By.XPATH, "//li[@data-id='remove']")