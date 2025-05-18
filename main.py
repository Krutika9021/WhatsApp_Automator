from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, os, re, sys
from webdriver_manager.chrome import ChromeDriverManager

COUNTRY_CODE = "91"
WAIT_FOR_LOGIN = 60
SEND_WAIT = 2
USER_DATA_DIR = os.path.abspath("chrome_automation_profile")  # Use dedicated profile
PROFILE_DIR = "Profile 1"
MESSAGE_FILE = "message.txt"
NUMBERS_FILE = "numbers.txt"

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument(f"--profile-directory={PROFILE_DIR}")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

# launching the Chrome here
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, WAIT_FOR_LOGIN)

# read phone numbers
if not os.path.exists(NUMBERS_FILE):
    print("❌ 'numbers.txt' not found!")
    sys.exit(1)
with open(NUMBERS_FILE, 'r') as f:
    phone_numbers = [re.sub(r'\D', '', line.strip()) for line in f if line.strip()]

# then msg
if not os.path.exists(MESSAGE_FILE):
    print("❌ 'message.txt' not found!")
    sys.exit(1)
with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
    message = f.read().strip()

driver.get("https://web.whatsapp.com")
print("🔄 Waiting for WhatsApp Web login...")

try:
    wait.until(EC.presence_of_element_located((By.ID, "side")))
    print("✅ Logged in successfully!")
except TimeoutException:
    print("❌ Login timeout. Please scan QR code in time.")
    driver.quit()
    sys.exit(1)

for number in phone_numbers:
    print(f"\n📨 Sending to: {number}")
    url = f"https://web.whatsapp.com/send?phone={COUNTRY_CODE}{number}&text={message}"
    driver.get(url)

    try:
    
        chat_loaded = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][aria-label][data-tab]'))
        )
        time.sleep(SEND_WAIT)
        chat_loaded.send_keys(Keys.ENTER)
        print(f"✅ Message sent to {number}")
        time.sleep(SEND_WAIT)
    except Exception as e:
        print(f"❌ Failed to send to {number}: {str(e)}")
        continue

print("\n🎉 All messages sent!")
input("Press ENTER to close browser...")
driver.quit()
