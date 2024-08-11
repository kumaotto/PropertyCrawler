import scrapy
from crawling_house.items import Post


class ScrapyBlogSpiderSpider(scrapy.Spider):
    name = 'scrapy_blog_spider'
    allowed_domains = ['suumo.jp']
    start_urls = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&cb=0.0&ct=15.0&mb=0&mt=9999999&md=07&md=08&md=09&md=10&ts=1&ts=3&et=10&cn=20&kz=1&tc=0400103&tc=0400901&shkr1=03&shkr2=03&shkr3=03&shkr4=03&ekInput=20110&nk=-1&tj=50&sngz=&po1=09']
    seen_urls = set()

    def parse(self, response):
        posts = response.css('.l-cassetteitem li')
        self.log(f'Found {len(posts)} posts')

        for post in response.css('.cassetteitem'):
            detail_url = post.css('a.js-cassette_link_href::attr(href)').get()

            # 既に処理したURLの場合はスキップ
            if detail_url in self.seen_urls:
                continue

            self.seen_urls.add(detail_url)

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

        # 最後のリンクが「次へ」のリンク
        next_page = response.css('.pagination-parts a::attr(href)').getall()[-1]
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
