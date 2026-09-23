APPIUM_SERVER = "http://127.0.0.1:4723"

APP_PATH = "/home/santosh/Downloads/app-release.apk"

CAPABILITIES = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "Android",
    "appium:app": APP_PATH,
    "appium:noReset": True,
}

APP_PACKAGE = "com.example.app"

USERNAME_FIELD = (APP_PACKAGE + ":id/username")
PASSWORD_FIELD = (APP_PACKAGE + ":id/password")
LOGIN_BUTTON = (APP_PACKAGE + ":id/login_button")
LOGGED_IN_MARKER = (APP_PACKAGE + ":id/home_title")
LOGIN_ERROR_TEXT = "Invalid username or password"
