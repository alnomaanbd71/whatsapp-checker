#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
whatsapp_checker.py

এই স্ক্রিপ্টটি একটি কমা-সেপারেটেড PHONE_LIST এনভায়রনমেন্ট ভেরিয়েবল (দেশ কোড ছাড়া নম্বরগুলো) থেকে নম্বরগুলো নিয়ে
WhatsApp Web-এ চেক করে কোন নম্বরগুলো WhatsApp-এ রেজিস্টার্ড আছে তা লোগে প্রিন্ট করবে।

ব্যবহার:
  PHONE_LIST="93777670441,93771228985,93761300216" python whatsapp_checker.py

প্রয়োজনীয় প্যাকেজ:
  selenium
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    # ১. পরিবেশ ভেরিয়েবল থেকে PHONE_LIST পড়ুন (কমা সেপারেটেড)
    phone_list = os.getenv("PHONE_LIST", "")
    if not phone_list:
        print("ERROR: PHONE_LIST environment variable is empty.")
        print("Usage: PHONE_LIST=\"93777670441,93771228985,...\" python whatsapp_checker.py")
        return

    numbers = [n.strip() for n in phone_list.split(",") if n.strip()]
    if not numbers:
        print("ERROR: PHONE_LIST-এ কোনো বৈধ নম্বর পাওয়া যায়নি।")
        return

    # ২. Chrome/Chromium অপশন সেটআপ
    chrome_options = Options()
    chrome_options.add_argument("--headless")              # হেডলেস মোডে চালান
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # যদি CHROME_BIN এনভায়রনমেন্ট ভেরিয়েবল সেট করা থাকে, বাইনারি লোকেশন হিসেবে সেট করুন
    chrome_bin = os.getenv("CHROME_BIN")
    if chrome_bin:
        chrome_options.binary_location = chrome_bin

    # ৩. WebDriver ইন্সট্যান্স তৈরি
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print("ERROR: Chrome WebDriver চালু করতে সমস্যা:", e)
        return

    # ৪. WhatsApp Web-এ লগইন
    print("WhatsApp Web এ লগইন করার জন্য QR কোড স্ক্যান করুন, তারপর Enter চাপুন...")
    driver.get("https://web.whatsapp.com/")
    input()  # ইউজার QR স্ক্যান করার জন্য অপেক্ষা

    open_on_whatsapp = []
    for num in numbers:
        url = f"https://web.whatsapp.com/send?phone={num}&text=&app_absent=0"
        driver.get(url)
        time.sleep(5)  # পেজ লোড হতে অপেক্ষা

        # “invalid number” এলার্ট আছে কিনা চেক
        try:
            driver.find_element(By.CSS_SELECTOR, "div[data-testid='alert-phone-number']")
            # এলার্ট পাওয়া গেলে: নম্বর রেজিস্টার নেই
        except:
            # এলার্ট না পাওয়া গেলে: নম্বর WhatsApp-এ আছে
            open_on_whatsapp.append("+" + num)

    # ৫. WebDriver বন্ধ
    driver.quit()

    # ৬. ফলাফল লোগে প্রিন্ট করুন
    print(f"\n✅ মোট {len(open_on_whatsapp)} টি নম্বর WhatsApp-এ রেজিস্টার্ড রয়েছে:\n")
    for num in open_on_whatsapp:
        print(num)

if __name__ == "__main__":
    main()
