import scrapy


class Post(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    rent = scrapy.Field()
    management_fee = scrapy.Field()
    security_deposit = scrapy.Field()
    reikin = scrapy.Field()
    age = scrapy.Field()
    address = scrapy.Field()
    station = scrapy.Field()
    floor = scrapy.Field()
    all_floor = scrapy.Field()
    area = scrapy.Field()
