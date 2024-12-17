import os

# Scrapy settings for scraping project
BOT_NAME = "scraping"

SPIDER_MODULES = ["scraping.spiders"]
NEWSPIDER_MODULE = "scraping.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Download settings
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# Autothrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Database Configuration
POSTGRESQL_URI = 'postgresql://Marjia:Marjia029@db:5432/trip'

# Enable the images pipeline
ITEM_PIPELINES = {
    'scraping.pipelines.HotelImagesPipeline': 300,
    'scraping.pipelines.PostgreSQLPipeline': 800,
}

# Set the location for saving images
IMAGES_STORE = '/app/images'  # Absolute path inside the container

# Enable logging for debugging
LOG_LEVEL = 'DEBUG'

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"