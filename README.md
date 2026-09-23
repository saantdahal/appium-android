# Appium Android Automation — Setup & Usage Guide

This documents how Appium is set up on this machine and how to run and extend
the test script in [test.py](test.py) for Android app automation.

## 1. What's installed

| Component | Version / Path |
|---|---|
| Appium server | `3.7.0` (`/usr/local/bin/appium`) |
| UiAutomator2 driver | `8.5.2` (installed via `appium driver install uiautomator2`) |
| Appium Python client | `/home/santosh/.local/lib/python3.14/site-packages/appium` |
| ADB | `1.0.41` |
| Appium Inspector | `~/Appium-Inspector-2026.9.2-linux-x86_64.AppImage` (desktop shortcut installed) |

Check drivers anytime with:
```bash
appium driver list --installed
```

## 2. Prerequisites before every run

1. **An Android device or emulator must be connected and visible to adb:**
   ```bash
   adb devices
   ```
   You should see something like:
   ```
   List of devices attached
   emulator-5554   device
   ```
   If nothing shows up, start an emulator (Android Studio → Device Manager, or
   `emulator -avd <name>`) or plug in / connect a real device with USB
   debugging enabled.

2. **The APK you want to test must exist at the path used in your script**
   (currently `/home/santosh/Downloads/app-release.apk` in [test.py](test.py)).

## 3. Installing the APK on the emulator manually

You normally **don't need this** — Appium installs the APK for you via the
`appium:app` capability in [test.py](test.py) every time a session starts.
Use manual install only when you want to test install/launch separately from
automation, or debug an install failure outside of Appium.

```bash
# Confirm the emulator is visible first
adb devices

# Install the APK
adb install /home/santosh/Downloads/app-release.apk
```

If the app is already installed and you want to overwrite it (keeping app
data):
```bash
adb install -r /home/santosh/Downloads/app-release.apk
```

If you get `INSTALL_FAILED_UPDATE_INCOMPATIBLE` (signature mismatch with an
existing install), uninstall first, then install fresh:
```bash
adb uninstall com.example.app   # use the real package name, see below
adb install /home/santosh/Downloads/app-release.apk
```

**Finding the package name** if you don't already know it:
```bash
aapt dump badging /home/santosh/Downloads/app-release.apk | grep package:\ name
```
(`aapt` ships with the Android SDK build-tools, e.g.
`~/Android/Sdk/build-tools/36.0.0/aapt`.)

**Launching the installed app manually** (without Appium), useful to sanity
check it runs at all:
```bash
adb shell monkey -p com.example.app -c android.intent.category.LAUNCHER 1
```

**Verifying install:**
```bash
adb shell pm list packages | grep com.example.app
```

## 4. Starting the Appium server

Appium is the middleman between your script and the device. It must be
running before any test script connects.

```bash
appium
```

This starts the server on `http://127.0.0.1:4723` by default. Leave this
running in its own terminal tab. You'll see:
```
[Appium] Welcome to Appium v3.7.0
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

Sanity check it's actually up (from another terminal):
```bash
curl -s http://127.0.0.1:4723/status
```
A healthy response looks like:
```json
{"value":{"ready":true,"message":"The server is ready to accept new connections", ...}}
```

If you see `Connection refused` when running a test script, it almost always
means this step was skipped.

## 5. Running the test script

```bash
python3 test.py
```

### What [test.py](test.py) does, line by line

```python
from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"        # target platform
options.automation_name = "UiAutomator2" # Android automation engine
options.device_name = "Android"          # logical device name (any string works for local runs)
options.app = "/home/santosh/Downloads/app-release.apk"  # APK to install & launch

driver = webdriver.Remote(
    "http://127.0.0.1:4723",  # Appium server address
    options=options
)

print("App launched!")

driver.quit()  # ends the session, uninstalls nothing but closes the driver
```

When run successfully, Appium will:
1. Install the APK on the connected device/emulator (if not already installed).
2. Launch the app.
3. Print `App launched!`.
4. Quit the driver session (this does **not** close the app on the device,
   it just ends the automation session).

## 6. Writing your own automation steps

Between `driver = webdriver.Remote(...)` and `driver.quit()`, add real
interactions. Example — tap a button and type into a field:

```python
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)

# Find by resource-id (most reliable — get this from Appium Inspector)
login_button = wait.until(
    EC.element_to_be_clickable((AppiumBy.ID, "com.example.app:id/login_button"))
)
login_button.click()

username_field = driver.find_element(AppiumBy.ID, "com.example.app:id/username")
username_field.send_keys("myuser")

# Find by accessibility id / text
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Submit").click()

# XPath (slower, use when no id/accessibility id is available)
driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Welcome']")
```

Common locator strategies (`AppiumBy`):
| Strategy | Use when |
|---|---|
| `AppiumBy.ID` | Element has a `resource-id` (fastest, most stable) |
| `AppiumBy.ACCESSIBILITY_ID` | Element has a `content-desc` |
| `AppiumBy.XPATH` | No id available, need to traverse structure |
| `AppiumBy.CLASS_NAME` | Matching by widget type, e.g. `android.widget.Button` |

## 7. Inspecting the app UI with Appium Inspector

Appium Inspector lets you click through the live app and copy element
locators (id, accessibility id, xpath) instead of guessing them.

1. Make sure the Appium server is running (step 4) and a device is connected
   (step 2).
2. Launch it from your app menu ("Appium Inspector") or the Desktop shortcut,
   or directly:
   ```bash
   ~/Appium-Inspector-2026.9.2-linux-x86_64.AppImage
   ```
   If it fails to launch due to sandboxing:
   ```bash
   ~/Appium-Inspector-2026.9.2-linux-x86_64.AppImage --no-sandbox
   ```
3. In the "Remote Host" section, use:
   - **Remote Host**: `127.0.0.1`
   - **Remote Port**: `4723`
   - Leave "Remote Path" blank (or `/`)
4. In "Desired Capabilities" → JSON Representation, paste:
   ```json
   {
     "platformName": "Android",
     "appium:automationName": "UiAutomator2",
     "appium:deviceName": "Android",
     "appium:app": "/home/santosh/Downloads/app-release.apk"
   }
   ```
5. Click **Start Session**. The app installs/launches on the device and you
   get a live screenshot with a clickable element tree on the right —
   selecting any element shows its `resource-id`, `content-desc`, `xpath`,
   and bounds, which you copy straight into your script.
6. Click **Quit Session** when done inspecting — only one Appium session (test
   script or Inspector) can hold the device at a time.

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ConnectionRefusedError` / `Max retries exceeded ... 4723` | Appium server not running | Run `appium` in a terminal, verify with `curl http://127.0.0.1:4723/status` |
| `python3: can't open file 'test_app.py'` | Wrong filename | The script is `test.py`, not `test_app.py` |
| `A new session could not be created` / driver not found | UiAutomator2 driver missing | `appium driver install uiautomator2` |
| `adb devices` shows nothing | No emulator/device connected | Start an emulator or connect a device with USB debugging on |
| App installs but instantly crashes | APK incompatible with device's Android version/ABI | Check `adb logcat` while it happens |
| Inspector can't find elements / blank tree | Wrong capabilities or app not actually in foreground | Re-check the `app` path capability; confirm `adb shell dumpsys window | grep mCurrentFocus` matches your app |

## 9. Project structure

```
appium/
├── README.md
├── conftest.py               # marks project root for pytest imports, keep empty
├── test.py                   # standalone quick-start smoke script (section 5)
├── core/
│   ├── __init__.py
│   ├── config.py             # server URL, app path, capabilities, login locators
│   └── login_flow.py         # create_driver(), login(), is_logged_in(), get_login_error_text()
├── tests/
│   ├── __init__.py
│   └── test_login.py         # pytest suite: valid login, wrong password, empty fields
└── notebooks/
    └── appium_login.ipynb    # interactive step-by-step login flow with inline screenshots
```

`core/` holds shared logic imported by both `tests/` and `notebooks/`.
`tests/` is picked up automatically by pytest. `notebooks/` is for
interactive/exploratory runs, not automated CI.

**Before running either**, update the placeholder values in
`core/config.py` — `APP_PACKAGE`, `USERNAME_FIELD`, `PASSWORD_FIELD`,
`LOGIN_BUTTON`, `LOGGED_IN_MARKER`, `LOGIN_ERROR_TEXT` — using Appium
Inspector (section 7) against your actual app's login screen. Everything
else in the project imports its locators from this file, so it's the only
place you need to edit.

**Running the pytest suite** (from the project root):
```bash
pytest
```

**Running the notebook:**
```bash
jupyter notebook notebooks/appium_login.ipynb
```
Both require the Appium server running and a device connected (sections 2 and 4).

## 10. Useful commands reference

```bash
# List connected devices/emulators
adb devices

# List installed Appium drivers
appium driver list --installed

# Install/update the UiAutomator2 driver
appium driver install uiautomator2

# Check Appium server health
curl -s http://127.0.0.1:4723/status

# Uninstall the app from the device (e.g. to force a fresh install)
adb uninstall com.example.app

# Stream device logs while a test runs
adb logcat
```
