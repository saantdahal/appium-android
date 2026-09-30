from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core import config


def create_driver(wait_timeout: int = 15):
    options = UiAutomator2Options().load_capabilities(config.CAPABILITIES)
    driver = webdriver.Remote(config.APPIUM_SERVER, options=options)
    wait = WebDriverWait(driver, wait_timeout)
    return driver, wait


def login(driver, wait, username: str, password: str) -> None:
    username_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, config.USERNAME_FIELD))
    )
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(AppiumBy.ID, config.PASSWORD_FIELD)
    password_field.clear()
    password_field.send_keys(password)

    driver.find_element(AppiumBy.ID, config.LOGIN_BUTTON).click()


def is_logged_in(driver, wait, timeout: int = 10) -> bool:
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.ID, config.LOGGED_IN_MARKER))
        )
        return True
    except Exception:
        return False


def get_login_error_text(driver) -> str | None:
    try:
        el = driver.find_element(
            AppiumBy.XPATH, f"//*[contains(@text, '{config.LOGIN_ERROR_TEXT}')]"
        )
        return el.text
    except Exception:
        return None


def open_forgot_password(driver, wait) -> None:
    link = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, config.FORGOT_PASSWORD_LINK))
    )
    link.click()


def request_password_reset(driver, wait, email: str) -> None:
    email_field = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, config.FORGOT_PASSWORD_EMAIL_FIELD))
    )
    email_field.clear()
    email_field.send_keys(email)

    driver.find_element(AppiumBy.ID, config.FORGOT_PASSWORD_SUBMIT_BUTTON).click()


def get_forgot_password_message_text(driver) -> str | None:
    try:
        el = driver.find_element(
            AppiumBy.XPATH,
            "//*[contains(@text, '{}') or contains(@text, '{}')]".format(
                config.FORGOT_PASSWORD_CONFIRMATION_TEXT,
                config.FORGOT_PASSWORD_ERROR_TEXT,
            ),
        )
        return el.text
    except Exception:
        return None
