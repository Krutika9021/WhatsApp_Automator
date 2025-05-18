from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import traceback

try:
    service = Service(r"D:\Project\WhatsApp-Automator\chromedriver.exe")  # update path if needed
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com")
    print("Opened Google successfully")

except Exception as e:
    print("Error occurred:")
    traceback.print_exc()
