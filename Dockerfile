# Ubuntu 20.04 বেস ইমেজ ব্যবহার করুন
FROM ubuntu:20.04

# ইন্টারএক্টিভ প্রম্পট এড়ান
ENV DEBIAN_FRONTEND=noninteractive

# Chrome এবং ChromeDriver-এর ভার্সন এক্সপ্লিসিটলি ডিফাইন করুন
ENV CHROME_VERSION="116.0.5845.96-1"
ENV CHROMEDRIVER_VERSION="116.0.5845.96"

# ডিপেন্ডেন্সি ইন্সটল করুন
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Google Chrome স্পেসিফিক ভার্সন ইন্সটল করুন
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -qqy --fix-missing && \
    apt-get -qqy install google-chrome-stable=${CHROME_VERSION} && \
    rm -rf /var/lib/apt/lists/*

# ChromeDriver স্পেসিফিক ভার্সন ইন্সটল করুন
RUN wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# ভার্সন ভেরিফিকেশন
RUN google-chrome --version && chromedriver --version

# আপনার অ্যাপ্লিকেশন সেটআপ এখানে যোগ করুন
# উদাহরণ:
# WORKDIR /app
# COPY . .
# CMD ["python3", "main.py"]
