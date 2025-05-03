FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# Chrome ও ChromeDriver ভার্সন সেট করুন
ENV CHROME_VERSION="136.0.7103.59-1"
ENV CHROMEDRIVER_VERSION="136.0.7103.59"

# ডিপেন্ডেন্সি ইন্সটল করুন
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Google Chrome ইন্সটল করুন
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -qqy && \
    apt-get install -y google-chrome-stable=${CHROME_VERSION} && \
    rm -rf /var/lib/apt/lists/*

# ChromeDriver ইন্সটল করুন
RUN wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# ভার্সন চেক করুন
RUN google-chrome --version && chromedriver --version
