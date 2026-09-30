import pytest

from core import config
from core.login_flow import (
    create_driver,
    login,
    is_logged_in,
    get_login_error_text,
    open_forgot_password,
    request_password_reset,
    get_forgot_password_message_text,
)

VALID_USERNAME = "testuser"
VALID_PASSWORD = "correct-password"
INVALID_PASSWORD = "wrong-password"

VALID_EMAIL = "testuser@example.com"


@pytest.fixture
def driver():
    drv, wait = create_driver()
    drv.wait = wait
    yield drv
    drv.quit()


def test_valid_login_succeeds(driver):
    login(driver, driver.wait, VALID_USERNAME, VALID_PASSWORD)
    assert is_logged_in(driver, driver.wait)


def test_invalid_password_shows_error(driver):
    login(driver, driver.wait, VALID_USERNAME, INVALID_PASSWORD)
    assert not is_logged_in(driver, driver.wait, timeout=5)
    assert get_login_error_text(driver) is not None


def test_empty_credentials_blocked(driver):
    login(driver, driver.wait, "", "")
    assert not is_logged_in(driver, driver.wait, timeout=5)


def test_forgot_password_valid_email_shows_confirmation(driver):
    open_forgot_password(driver, driver.wait)
    request_password_reset(driver, driver.wait, VALID_EMAIL)

    message = get_forgot_password_message_text(driver)
    assert message is not None
    assert config.FORGOT_PASSWORD_CONFIRMATION_TEXT in message


def test_forgot_password_empty_email_shows_error(driver):
    open_forgot_password(driver, driver.wait)
    request_password_reset(driver, driver.wait, "")

    message = get_forgot_password_message_text(driver)
    assert message is None or config.FORGOT_PASSWORD_ERROR_TEXT in message
