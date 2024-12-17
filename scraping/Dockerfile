FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables to fix module import
ENV SCRAPY_SETTINGS_MODULE=scraping.settings
ENV PYTHONPATH="/app:/app/scraping"

# Create directories for images and logs
RUN mkdir -p /app/images /app/logs

# Command to run the spider
CMD ["scrapy", "crawl", "random_city_hotels_crawl_scraper"]
