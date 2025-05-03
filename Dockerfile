# Dockerfile

# 1. Base image
FROM python:3.11-slim

# 2. Install system dependencies, Xvfb, xauth, and Google Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    x11-xauth \
    xvfb \
    fonts-liberation \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libxi6 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libxtst6 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libappindicator3-1 \
    xdg-utils \
  && rm -rf /var/lib/apt/lists/*

# Add Google’s signing key and repo, then install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update && apt-get install -y --no-install-recommends google-chrome-stable \
  && rm -rf /var/lib/apt/lists/*

# 3. Define working directory
WORKDIR /app

# 4. Copy application code
COPY . /app

# 5. Install Python dependencies (including webdriver-manager)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Tell Selenium where Chrome lives
ENV CHROME_BIN=/usr/bin/google-chrome-stable

# 7. Expose Flask port
EXPOSE 5000

# 8. Default command: run Flask under Xvfb
CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "python", "main.py"]
