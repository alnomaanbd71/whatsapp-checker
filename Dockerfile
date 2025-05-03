FROM python:3.11-slim

# 1) Install Chromium + driver + deps
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    wget \
    unzip \
    libxi6 libgconf-2-4 libnss3 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxrandr2 \
    libxss1 libxtst6 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libpangocairo-1.0-0 libcairo2 \
    fonts-liberation libappindicator3-1 xdg-utils \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# let selenium know where Chromium lives
ENV CHROME_BIN=/usr/bin/chromium
# Render will set $PORT for you
ENV PORT=5000

# run Flask
EXPOSE 5000
CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "python", "main.py"]
