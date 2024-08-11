from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawling_batch.crawling_house.spiders.scrapy_blog_spider import ScrapyBlogSpiderSpider


def lambda_handler(event, context):
    process = CrawlerProcess(get_project_settings())
    process.crawl(ScrapyBlogSpiderSpider)
    process.start()
    return {'statusCode': 200, 'body': 'Scrapy crawl completed'}
