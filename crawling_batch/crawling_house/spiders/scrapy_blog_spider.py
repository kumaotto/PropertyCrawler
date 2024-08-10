import scrapy
from crawling_house.items import Post


class ScrapyBlogSpiderSpider(scrapy.Spider):
    name = 'scrapy_blog_spider'
    allowed_domains = ['suumo.jp']
    start_urls = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&fw2=&pc=30&po1=09&po2=99&ta=13&md=07&md=08&md=09&md=10&ts=1&cb=0.0&ct=15.5&et=10&mb=0&mt=9999999&cn=20&ekInput=84580&ekInput=26650&nk=-1&nk=-1&tj=80&tj=80&co=1&kz=1&tc=0401303&tc=0400101&tc=0400301&tc=0400901&shkr1=03&shkr2=03&shkr3=03&shkr4=03']

    def parse(self, response):
        posts = response.css('.l-cassetteitem li')
        self.log(f'Found {len(posts)} posts')

        for post in response.css('.cassetteitem'):
            detail_url = post.css('a.js-cassette_link_href::attr(href)').get()

            yield Post(
                url=response.urljoin(detail_url) if detail_url else None,
                title=post.css('.cassetteitem_content-title::text').get().strip(),
                image_url=post.css('img.js-noContextMenu.js-linkImage.js-adjustImg::attr(rel)').get(),
                rent=post.css('span.cassetteitem_other-emphasis.ui-text--bold::text').get(),
                management_fee=post.css('span.cassetteitem_price.cassetteitem_price--administration::text').get(),
                security_deposit=post.css('span.cassetteitem_price.cassetteitem_price--deposit::text').get(),
                reikin=post.css('span.cassetteitem_price.cassetteitem_price--gratuity::text').get(),
                age=post.xpath('.//li[contains(@class, "cassetteitem_detail-col3")]/div[1]/text()').get(),
                address=post.css('li.cassetteitem_detail-col1::text').get().strip(),
                station=post.xpath('.//li[contains(@class, "cassetteitem_detail-col2")]//div[contains(@class, "cassetteitem_detail-text")][1]/text()').get().strip(),
                floor=post.xpath('.//tr[contains(@class, "js-cassette_link")]/td[3]/text()').get().strip(),
                all_floor=post.xpath('.//li[contains(@class, "cassetteitem_detail-col3")]/div[2]/text()').get().strip(),
                area=post.css('span.cassetteitem_menseki::text').get().strip(),
            )
