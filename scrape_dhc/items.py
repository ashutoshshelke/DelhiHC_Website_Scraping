# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeDhcItem(scrapy.Item):
    # define the fields for your item here like:
    #headers = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    srno = scrapy.Field()
    diaryno = scrapy.Field()
    status = scrapy.Field()
    petitioner_vs_respondent = scrapy.Field()
    listing_date = scrapy.Field()
    #_id = scrapy.Field()
