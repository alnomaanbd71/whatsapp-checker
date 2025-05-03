# Dockerfile

FROM python:3.11-slim

# 1. Install Chromium Browser, ChromeDriver, Xvfb, xauth and required libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium-browser \
    chromium-chromedriver \
    xvfb \
    x11-xauth \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libpangocairo-1.0-0 \
    libcairo2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
  && rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy application code
COPY . /app

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tell Selenium where to find the Chromium binary
ENV CHROME_BIN=/usr/bin/chromium-browser

# 6. Expose the Flask listening port
EXPOSE 5000

# 7. Default command: run Flask under Xvfb
CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "python", "main.py"]
