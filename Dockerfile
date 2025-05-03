FROM python:3.11-slim

# 1) Install Chromium & driver + dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    libxi6 libgconf-2-4 libnss3 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxrandr2 \
    libxss1 libxtst6 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libpangocairo-1.0-0 libcairo2 \
    fonts-liberation libappindicator3-1 xdg-utils \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# 2) Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# 3) Tell Selenium where chromium is
ENV CHROME_BIN=/usr/bin/chromium

# 4) Expose the port Flask will listen on
EXPOSE 5000

# 5) Default command
CMD ["xvfb-run", "--server-args=-screen 0 1024x768x24", "python", "main.py"]
