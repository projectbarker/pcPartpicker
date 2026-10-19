# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from datetime import datetime, timezone
import logging
import os
from random import randint
from urllib.parse import urlencode

import requests
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BatchSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class PlaywrightProxyMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.username = settings.get('PROXY_USER')
        self.password = settings.get('PROXY_PASSWORD')
        self.url = settings.get('PROXY_URL')
        self.port = settings.get('PROXY_PORT')

    def process_request(self, request, spider):
        if 'playwright' in request.meta:
            # proxy_url = f'http://customer-{self.username}:{self.password}@{self.url}:{self.port}'
            request.meta["playwright_context"]="proxy"
            request.meta["playwright_include_page"]=True
            proxy_config = {
                "server": f'{self.url}:{self.port}',
                "username": self.username,
                "password": self.password
            }
            request.meta["playwright_context_kwargs"] = {"proxy": proxy_config}
        return None

class FakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = 'https://headers.scrapeops.io/v1/browser-headers'
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = 200
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True

    # def process_request(self, request, spider):
    #
    #     random_browser_header = self._get_random_browser_header()
    #     request.headers['accept-language'] = random_browser_header['accept-language']
    #     request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user']
    #     request.headers['sec-fetch-mode'] = random_browser_header['sec-fetch-mode']
    #     request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site']
    #     request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform']
    #     request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile']
    #     request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua']
    #     request.headers['accept'] = random_browser_header['accept']
    #     request.headers['user-agent'] = random_browser_header['user-agent']
    #     request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')
    #     logging.log(logging.INFO, "************ NEW HEADER ATTACHED *******\n"+random_browser_header['user-agent'])

    def process_request(self, request, spider):
        random_browser_header = self._get_random_browser_header()

        # Safely set headers using .get() and provide default values where necessary
        request.headers['accept-language'] = random_browser_header.get('accept-language', 'en-US')
        request.headers['sec-fetch-user'] = random_browser_header.get('sec-fetch-user', '?1')
        request.headers['sec-fetch-mode'] = random_browser_header.get('sec-fetch-mode', 'navigate')
        request.headers['sec-fetch-site'] = random_browser_header.get('sec-fetch-site', 'same-site')
        request.headers['sec-ch-ua-platform'] = random_browser_header.get('sec-ch-ua-platform', 'macOS')
        request.headers['sec-ch-ua-mobile'] = random_browser_header.get('sec-ch-ua-mobile', '?0')
        request.headers['sec-ch-ua'] = random_browser_header.get('sec-ch-ua','"Chromium";v="92", "Google Chrome";v="92", "Not A Brand";v="99"')
        request.headers['accept'] = random_browser_header.get('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
        request.headers['user-agent'] = random_browser_header.get('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests', '1')

        logging.log(logging.INFO, "************ NEW HEADER ATTACHED *******\n" + random_browser_header.get('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'))