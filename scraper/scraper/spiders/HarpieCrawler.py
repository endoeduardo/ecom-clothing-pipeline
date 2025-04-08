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
        
        for link in links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_page,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "load")
                    ]
                }
            )

    def parse_page(self, response: Response):
        """Follow the product links"""
        products = response.xpath(".//div[@id='lista-produtos-area']//li")
        for product in products:
            product_link = product.xpath(".//a/@href").get()
            if product_link:
                yield scrapy.Request(
                    url=response.urljoin(product_link),
                    callback=self.parse_item,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_load_state", "load")
                        ]
                    }
                )

        next_page = response.xpath(".//li[@class='nav']/a[contains(text(),'Próxima')]/@href").get()
        if next_page is not None:
            yield scrapy.Request(
                    url=response.urljoin(next_page),
                    callback=self.parse_page,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_load_state", "load")
                        ]
                    }
                )
    
    def parse_item(self, response: Response):
        """Parse the product item and returns a JSON with the parsing data"""
        yield {
            "product_name": response.xpath(".//h1/text()").get(),
            "pix_price": response.xpath(".//div[@class='preco-pix']/strong/text()").get(),
            "gender": response.xpath(".//dt[contains(text(), 'Gênero')]/following-sibling::dd/text()").get()
        }
