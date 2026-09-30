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

FORGOT_PASSWORD_LINK = (APP_PACKAGE + ":id/forgot_password_link")
FORGOT_PASSWORD_EMAIL_FIELD = (APP_PACKAGE + ":id/email")
FORGOT_PASSWORD_SUBMIT_BUTTON = (APP_PACKAGE + ":id/submit_button")
FORGOT_PASSWORD_CONFIRMATION_TEXT = "Password reset link sent"
FORGOT_PASSWORD_ERROR_TEXT = "No account found with that email"
