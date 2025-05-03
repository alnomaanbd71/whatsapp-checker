# Dockerfile

# 1. Base image
FROM python:3.11-slim

# 2. Install Chromium, Chromedriver, Xvfb, xauth and required libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    xvfb \
    x11-xauth \                  # ← provides the xauth command
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

# 3. Set working directory
WORKDIR /app

# 4. Copy application code
COPY . /app

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Environment variable for Selenium
ENV CHROME_BIN=/usr/bin/chromium

# 7. Expose Flask port
EXPOSE 5000

# 8. Default command: run Flask under Xvfb
CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "python", "main.py"]
