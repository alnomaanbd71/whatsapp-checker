# Dockerfile

FROM python:3.11-slim

# Install Chromium, Chromedriver, Xvfb, xauth, and necessary libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
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

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Tell Selenium where to find Chromium
ENV CHROME_BIN=/usr/bin/chromium

# Expose the Flask listening port
EXPOSE 5000

# Start the Flask app under Xvfb
CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "python", "main.py"]
