#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main.py

Flask-based Web UI & API for WhatsApp Number Checker.

Provides:
 - GET  /        → HTML form with purple gradient, animated button
 - POST /check   → Accepts comma-separated numbers, runs Selenium check, renders results
 - JSON support if “Accept: application/json” in headers

Usage (development):
  export CHROME_BIN="/usr/bin/chromium"
  export PORT=5000
  python main.py

In Docker/Render:
  PORT injected by environment (default 5000)
"""

import os
from flask import Flask, request, render_template_string, jsonify
from whatsapp_checker import check_numbers

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
{{ result.registered | join('\n') }}

Not Registered:
{{ result.not_registered | join('\n') }}
      </pre>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(INDEX_HTML)

@app.route("/check", methods=["POST"])
def check():
    # Parse comma-separated input
    data = request.form.get("numbers", "")
    numbers = [n.strip() for n in data.split(",") if n.strip()]

    # Get Chromium binary path from environment
    chrome_bin = os.getenv("CHROME_BIN")

    # Perform the WhatsApp registration check
    registered, not_registered = check_numbers(numbers, chrome_bin=chrome_bin)

    # Return JSON if requested
    if request.headers.get("Accept", "").lower().startswith("application/json"):
        return jsonify({
            "registered": registered,
            "not_registered": not_registered
        })

    # Otherwise render HTML with results
    return render_template_string(
        INDEX_HTML,
        result={"registered": registered, "not_registered": not_registered}
    )

if __name__ == "__main__":
    # Listen on all interfaces, port from environment or default 5000
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
