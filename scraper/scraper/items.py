"""Define here the models for your scraped items

    See documentation in:
    https://docs.scrapy.org/en/latest/topics/items.html
"""
from scrapy import Item, Field

class ClothingItem(Item):
    """

    Attributes:
        product_name (scrapy.Field): The name of the product.
        product_link (scrapy.Field): The URL to the product's detail page.
        product_description (scrapy.Field): A description of the product.
        SKU (scrapy.Field): The product's unique SKU identifier.
        one_time_payment (scrapy.Field): The price if purchased as a one-time payment.
        quantity_of_payments (scrapy.Field): The number of installment payments available.
        payments_value (scrapy.Field): The value of each installment payment.
        color (scrapy.Field): The color of the product, if applicable.
        variation (scrapy.Field): Any variations of the product, such as size or style.
        rating (scrapy.Field): The average customer rating for the product.
        number_of_ratings (scrapy.Field): The total number of ratings the product has received.

    This item model is intended for use with Scrapy and helps in organizing 
    the structure of scraped data.
    """
    timestamp = Field()
    job_id = Field()
    site_name = Field()
    product_name = Field()
    internal_id = Field()
    price = Field()
    gender = Field()
    color = Field()
    category = Field()
