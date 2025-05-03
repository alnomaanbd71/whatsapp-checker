import os
from flask import Flask, request, render_template_string, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Checker</title>
        <style>
            body {
                background: linear-gradient(to right, #7b2ff7, #f107a3);
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            input[type=file], input[type=submit] {
                margin-top: 20px;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            input[type=submit] {
                background: #fff;
                color: #7b2ff7;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            input[type=submit]:hover {
                background: #f107a3;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>📱 WhatsApp Number Checker</h1>
        <form action="/check" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv" required>
            <br>
            <input type="submit" value="Check WhatsApp Numbers">
        </form>
    </body>
    </html>
    ''')

@app.route('/check', methods=['POST'])
def check():
    uploaded_file = request.files['file']
    df = pd.read_csv(uploaded_file)
    numbers = df['number'].astype(str).tolist()

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    results = []

    for number in numbers:
        driver.get(f"https://api.whatsapp.com/send?phone={number}")
        if "Use WhatsApp Web" in driver.page_source:
            results.append((number, "Registered"))
        else:
            results.append((number, "Not Registered"))

    driver.quit()

    result_df = pd.DataFrame(results, columns=["Number", "Status"])
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    result_df.to_excel(temp_file.name, index=False)

    return send_file(temp_file.name, as_attachment=True, download_name="whatsapp_checked.xlsx")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
