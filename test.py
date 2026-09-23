from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "Android"
options.app = "/home/santosh/Downloads/app-release.apk"

driver = webdriver.Remote(
    "http://127.0.0.1:4723",
    options=options
)

print("App launched!")

driver.quit()