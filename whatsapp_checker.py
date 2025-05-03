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
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(
        service=Service(executable_path='/usr/local/bin/chromedriver'),
        options=chrome_options
    )
    
    registered, not_registered = [], []
    
    for num in numbers:
        try:
            driver.get(f"https://wa.me/{num}")
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            if "invalid" in driver.page_source.lower():
                not_registered.append(num)
            else:
                registered.append(num)
        except TimeoutException:
            not_registered.append(num)
        except Exception as e:
            not_registered.append(num)
    
    driver.quit()
    
    df = pd.DataFrame({
        "Registered Numbers": registered,
        "Unregistered Numbers": not_registered
    })
    
    output_path = f"/tmp/{task_id}.xlsx"
    df.to_excel(output_path, index=False)
    return output_path

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/check")
async def check(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    numbers = df['phone'].astype(str).tolist()
    task_id = str(uuid.uuid4())
    output_path = check_whatsapp_numbers(numbers, task_id)
    return {"download_url": f"/download/{task_id}"}

@app.get("/download/{task_id}")
async def download(task_id: str):
    return FileResponse(
        f"/tmp/{task_id}.xlsx",
        filename="whatsapp_results.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
