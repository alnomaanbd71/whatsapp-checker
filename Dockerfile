# Dockerfile (updated)

FROM python:3.11-slim

# ১) সিস্টেম ডিপেন্ডেন্সি ও Chromium+Driver ইনস্টল
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    wget \
    unzip \
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

# ২) কাজের ডিরেক্টরি সেট এবং সোর্স কপি
WORKDIR /app
COPY . /app

# ৩) Python requirements ইনস্টল
RUN pip install --no-cache-dir -r requirements.txt

# ৪) ENTRYPOINT: Xvfb + Chromium headless
#    আমরা selenium এ browser path ও driver path দেবো
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

ENTRYPOINT ["/usr/bin/xvfb-run", "--server-args=-screen 0 1024x768x24", "python", "whatsapp_checker.py"]
