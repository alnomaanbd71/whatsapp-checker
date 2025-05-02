FROM python3.11-slim

# Chrome ও chromedriver ইন্সটল
RUN apt-get update && 
    apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libnss3 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxrandr2 libxss1 libxtst6 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libpangocairo-1.0-0 libpangocairo-1.0-0 libcairo2 && 
    wget -q httpsdl.google.comlinuxdirectgoogle-chrome-stable_current_amd64.deb && 
    apt install -y .google-chrome-stable_current_amd64.deb && 
    CHROME_VERSION=$(google-chrome --product-version) && 
    CHROME_MAJOR=$(echo $CHROME_VERSION  cut -d'.' -f1) && 
    wget -q httpschromedriver.storage.googleapis.com${CHROME_MAJOR}.0.0.0chromedriver_linux64.zip && 
    unzip chromedriver_linux64.zip -d usrbin && 
    chmod +x usrbinchromedriver && 
    rm .zip .deb

WORKDIR app
COPY . app
RUN pip install --no-cache-dir -r requirements.txt

# অফিশিয়াল SlackWebhook এ লোগ করতে Xvfb ব্যাবহার
ENTRYPOINT [usrbinxvfb-run, python, whatsapp_checker.py]