from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def check_whatsapp_numbers(numbers, task_id):
    os.makedirs('/tmp', exist_ok=True)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(
        service=Service('/usr/local/bin/chromedriver'),
        options=chrome_options
    )
    
    registered, not_registered = [], []
    
    for num in numbers:
        try:
            driver.get(f"https://wa.me/{num}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            if "invalid" in driver.page_source.lower():
                not_registered.append(num)
            else:
                registered.append(num)
        except TimeoutException:
            not_registered.append(num)
    
    driver.quit()
    
    df = pd.DataFrame({
        "Registered": registered,
        "Not Registered": not
