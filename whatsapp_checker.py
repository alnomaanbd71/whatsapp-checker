from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

# নম্বরগুলো তালিকা হিসেবে
numbers = os.getenv("PHONE_LIST", "").split(",")

# Chrome headless অপশন
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Chromedriver path (Render এ `/usr/bin/chromedriver`)
driver = webdriver.Chrome(options=chrome_options)

def main():
    driver.get("https://web.whatsapp.com/")
    print("QR স্ক্যান করে এন্টার চাপুন...")
    input()

    open_on_whatsapp = []
    for num in numbers:
        url = f"https://web.whatsapp.com/send?phone={num}&text=&app_absent=0"
        driver.get(url)
        time.sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR, "div[data-testid='alert-phone-number']")
        except:
            open_on_whatsapp.append("+" + num)

    driver.quit()
    df = pd.DataFrame({"WhatsApp ওপেন নম্বর": open_on_whatsapp})
    df.to_csv("whatsapp_open_numbers.csv", index=False, encoding="utf-8-sig")
    print(f"{len(open_on_whatsapp)} টি নম্বর CSV এ সেভ হয়েছে।")

if __name__ == "__main__":
    main()