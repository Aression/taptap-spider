# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RankItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    stat = scrapy.Field()


class CategoryItem(scrapy.Item):
    name = scrapy.Field()
    id = scrapy.Field()
    img_url = scrapy.Field()

    price = scrapy.Field
    stat = scrapy.Field()
    tags = scrapy.Field()
    downloads = scrapy.Field()

class GameDetailItem(scrapy.Item):
    name = scrapy.Field()
    # todo: check elements provided by the api and define proper fields