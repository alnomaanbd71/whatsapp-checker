FROM python:3.11-slim

# Chrome ও chromedriver ইন্সটল
RUN apt-get update && \
    apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libnss3 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxrandr2 libxss1 libxtst6 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libpangocairo-1.0-0 libcairo2 && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    CHROME_VERSION=$(google-chrome --product-version) && \
    CHROME_MAJOR=$(echo $CHROME_VERSION | cut -d'.' -f1) && \
    wget -q https://chromedriver.storage.googleapis.com/${CHROME_MAJOR}.0.0.0/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin/ && \
    chmod +x /usr/bin/chromedriver && \
    rm *.zip *.deb

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/usr/bin/xvfb-run", "python", "whatsapp_checker.py"]
