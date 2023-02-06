from decouple import config

BOT_NAME = 'cluster'

SPIDER_MODULES = ['cluster.spiders']
NEWSPIDER_MODULE = 'cluster.spiders'

SCRAPEOPS_API_KEY = config('SCRAPEOPS_API_KEY')
SCRAPEOPS_PROXY_ENABLED = True


DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
