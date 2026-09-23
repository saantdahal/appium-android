import pytest

from core.login_flow import create_driver, login, is_logged_in, get_login_error_text

VALID_USERNAME = "testuser"
VALID_PASSWORD = "correct-password"
INVALID_PASSWORD = "wrong-password"


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
