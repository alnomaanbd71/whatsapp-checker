#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py

Flask-based Web UI & API for WhatsApp Number Checker, using webdriver-manager
to install the correct ChromeDriver at runtime.

Endpoints:
 - GET  /        → HTML form with purple gradient & animated button
 - POST /check   → Accepts comma-separated numbers, runs Selenium check, renders results
 - JSON support if “Accept: application/json” in headers

Usage (development):
  export PORT=5000
  export CHROME_BIN="/usr/bin/google-chrome-stable"   # or "/usr/bin/chromium"
  python main.py

In Docker/Render:
  PORT injected by environment
"""

import os
import time
from flask import Flask, request, render_template_string, jsonify

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>WhatsApp Number Checker</title>
  <style>
    body {
      margin: 0; font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #7f00ff, #e100ff);
      height: 100vh; display: flex;
      align-items: center; justify-content: center;
    }
    .card {
      background: #fff; padding: 2rem; border-radius: 1rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
      width: 90%; max-width: 400px; text-align: center;
    }
    textarea {
      width: 100%; height: 100px; margin-bottom: 1rem;
      padding: 0.5rem; font-size: 1rem; border: 1px solid #ccc;
      border-radius: 0.5rem; resize: vertical;
    }
    button {
      width: 100%; padding: 0.75rem; font-size: 1rem;
      border: none; color: #fff;
      background: linear-gradient(90deg, #9c27b0, #e040fb);
      border-radius: 0.5rem; cursor: pointer;
      transition: transform .2s;
    }
    button:hover { transform: scale(1.03); }
    pre {
      background: #f4f4f4; padding: 1rem; border-radius: 0.5rem;
      text-align: left; overflow-x: auto; margin-top: 1rem;
    }
  </style>
</head>
<body>
  <div class="card">
    <h2>WhatsApp Number Checker</h2>
    <form method="post" action="/check">
      <textarea name="numbers" placeholder="e.g. 93777670441,93771228985,…"></textarea>
      <button type="submit">Check Numbers</button>
    </form>
    {% if result %}
      <h3>Result:</h3>
      <pre>
Registered:
{{ result.registered | join('\\n') }}

Not Registered:
{{ result.not_registered | join('\\n') }}
      </pre>
    {% endif %}
  </div>
</body>
</html>
"""

def check_numbers(numbers):
    """
    Given a list of digit-only phone numbers (no '+' prefix),
    returns two lists: (registered, not_registered).
    """
    chrome_bin = os.getenv("CHROME_BIN")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if chrome_bin:
        chrome_options.binary_location = chrome_bin

    # Use webdriver-manager to install matching ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to WhatsApp Web and wait for QR scan
    driver.get("https://web.whatsapp.com/")
    print("Please scan the QR code in WhatsApp Web and press Enter in the console...")
    input()

    registered = []
    not_registered = []

    for num in numbers:
        driver.get(f"https://web.whatsapp.com/send?phone={num}&text=&app_absent=0")
        time.sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR, "div[data-testid='alert-phone-number']")
            not_registered.append(f"+{num}")
        except:
            registered.append(f"+{num}")

    driver.quit()
    return registered, not_registered

@app.route("/", methods=["GET"])
def home():
    return render_template_string(INDEX_HTML)

@app.route("/check", methods=["POST"])
def check():
    data = request.form.get("numbers", "")
    numbers = [n.strip() for n in data.split(",") if n.strip()]

    registered, not_registered = check_numbers(numbers)

    if request.headers.get("Accept", "").lower().startswith("application/json"):
        return jsonify({
            "registered": registered,
            "not_registered": not_registered
        })

    return render_template_string(
        INDEX_HTML,
        result={"registered": registered, "not_registered": not_registered}
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
