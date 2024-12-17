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

# Item Pipelines
ITEM_PIPELINES = {
    'scraping.pipelines.HotelImagesPipeline': 300,
    'scraping.pipelines.DatabasePipeline': 800,
}

# Images storage settings (Absolute path to images folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_STORE = '/app/images'  # Absolute path for images folder
IMAGES_URLS_FIELD = 'image'
IMAGES_RESULT_FIELD = 'image_local_path'

# Advanced Reactor and Encoding Settings
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
