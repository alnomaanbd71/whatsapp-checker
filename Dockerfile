# Dockerfile

FROM python:3.11-slim

# ১) সাধারণ ডিপেন্ডেন্সি ইনস্টল
RUN apt-get update && apt-get install -y \
    wget gnupg unzip xvfb libxi6 libgconf-2-4 libnss3 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxrandr2 libxss1 \
    libxtst6 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libpangocairo-1.0-0 libcairo2 fonts-liberation libappindicator3-1 \
    xdg-utils \
  && rm -rf /var/lib/apt/lists/*

# ২) Google Chrome-এর GPG key ও রেপো যুক্ত করে Chrome ইনস্টল
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable \
  && rm -rf /var/lib/apt/lists/*

# ৩) Chrome-এর মেজর ভার্সনের সাথে মিলে তার উপযোগী chromedriver ইনস্টল
RUN CHROME_MAJOR="$(google-chrome --product-version | cut -d'.' -f1)" \
  && wget -q "https://chromedriver.storage.googleapis.com/${CHROME_MAJOR}.0.0.0/chromedriver_linux64.zip" \
  && unzip chromedriver_linux64.zip -d /usr/bin/ \
  && chmod +x /usr/bin/chromedriver \
  && rm chromedriver_linux64.zip

# ৪) অ্যাপ্‌ ডিরেক্টরি সেট করে কোড কপি ও প্রয়োজনীয় প্যাকেজ ইনস্টল
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# ৫) Xvfb দিয়ে স্ক্রিপ্ট রান
ENTRYPOINT ["/usr/bin/xvfb-run", "python", "whatsapp_checker.py"]
