# whatsapp_checker.py

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def check_numbers(numbers, chrome_bin=None):
    """
    Takes a list of strings (digits-only, no '+'). Returns two lists:
      (registered_numbers, not_registered_numbers)
    """
    # set up headless Chrome/Chromium
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    if chrome_bin:
        opts.binary_location = chrome_bin

    driver = webdriver.Chrome(options=opts)

    # login
    driver.get("https://web.whatsapp.com/")
    print("QR code for WhatsApp Web — scan and then press Enter")
    input()

    registered = []
    not_registered = []

    for num in numbers:
        url = f"https://web.whatsapp.com/send?phone={num}&text=&app_absent=0"
        driver.get(url)
        time.sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR, "div[data-testid='alert-phone-number']")
            not_registered.append(f"+{num}")
        except:
            registered.append(f"+{num}")

    driver.quit()
    return registered, not_registered
