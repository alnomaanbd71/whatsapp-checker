# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -qqy --fix-missing && \
    apt-get -qqy install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver dynamically based on Chrome version
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) && \
    wget -q "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION" -O LATEST_RELEASE && \
    CHROMEDRIVER_VERSION=$(cat LATEST_RELEASE) && \
    wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip LATEST_RELEASE

# Optional: Verify installations
RUN google-chrome --version && chromedriver --version

# Continue with your application setup
# (Add your application-specific steps below)
# Example:
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
# CMD ["python", "main.py"]
