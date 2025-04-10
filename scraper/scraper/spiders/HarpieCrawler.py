"""Harpie Crawler"""
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
    def __init__(self, timestamp=None, job_id=None):
        super().__init__()
        self.timestamp = timestamp
        self.job_id = job_id

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

        # links = links[4] # Testing purposes comment before going prod
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
    def extract_category(self, response: Response):
        """Extract and returns the category queried"""
        try:
            if response.request.url is not None and isinstance(response.request.url, str):
                category = response.request.url
                category = category.split("/")
                category = category[-1]
                return category
            return None
        except:
            return None
            
    def parse_item(self, response: Response):
        """Parse the product item and returns a JSON with the parsing data"""
        yield {
            "timestamp": self.timestamp,
            "job_id": self.job_id,
            "product_name": response.xpath(".//h1/text()").get(),
            "internal_id": response.xpath(".//div[@class='codigo-prod']/text()").get(),
            "price": response.xpath(".//div[@class='preco-pix']/strong/text()").get(),
            "gender": response.xpath(".//dt[contains(text(), 'Gênero')]/following-sibling::dd/text()").get(),
            "color": response.xpath(".//dt[contains(text(), 'Cor')]/following-sibling::dd/text()").get(),
            "category": self.extract_category(response)
        }
