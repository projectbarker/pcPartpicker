"""Minimal Scrapy settings for the Selenium-backed collector."""

BOT_NAME = "batch"
SPIDER_MODULES = ["batch.spiders"]
NEWSPIDER_MODULE = "batch.spiders"

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_TIMEOUT = 30
RETRY_ENABLED = False
AUTOTHROTTLE_ENABLED = False

# Browser navigation is owned by the spider. These unused handlers and
# middlewares previously caused hidden startup network calls and dependencies.
DOWNLOADER_MIDDLEWARES = {}
ITEM_PIPELINES = {}
FEED_EXPORT_ENCODING = "utf-8"
