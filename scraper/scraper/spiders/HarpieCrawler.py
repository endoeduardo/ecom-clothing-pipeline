"""Harpie Crawler"""
import re

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Response
from scrapy_playwright.page import PageMethod


class HarpieSpider(CrawlSpider):
    """Spider that crawls the harpie website"""
    name = "harpie_spider"
    # allowed_domains = ["https://www.harpie.com.br/"]
    # start_urls = ["https://www.harpie.com.br/"]
    BASE_URL = "https://www.harpie.com.br/"

    def start_requests(self):
        # start_urls = ["https://www.harpie.com.br/"]
        
        yield scrapy.Request(
            self.BASE_URL,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "load")
                ],
                "playwright_context": "default"
            },
            callback=self.parse
        )

    def parse(self, response: Response):
        """Extract and follow main links"""
        links = response.xpath(".//ul[@id='nav-root']/li//a/@href").getall()
        yield from response.follow_all(links, callback=self.parse_page)
    
    def parse_page(self, response: Response):
        products = response.xpath(".//div[@id='lista-produtos-area']//li")
        
        for product in products:
            product_link = product.xpath(".//a/@href").get()
            if product_link:
                yield response.follow(product_link, callback=self.parse_item)

        next_page = response.xpath(".//li[@class='nav']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_page)
    
    def parse_item(self, response: Response):
        yield {
            "product_name": response.xpath(".//h1/text()").get()
        }
