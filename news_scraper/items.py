# The models for the scraped data are defined here.
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    topic = scrapy.Field()
    related_topics = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    pass
