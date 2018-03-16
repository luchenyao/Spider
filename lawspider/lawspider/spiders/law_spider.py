# coding=utf-8

import scrapy

class Post(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()

class LawSpider(scrapy.Spider):
    name = 'law'

    def start_requests(self):
        urls = [
            'http://www.spp.gov.cn/spp/sscx/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//div[@class="detail_tit"]/text()').extract_first()
        if title:
            sub_posts = []
            for line in response.xpath('//div[@class="TRS_Editor"]//p'):
                if line.xpath('./@align').extract():
                    sub_posts.append({})
                    sub_posts[-1]['sub_title'] = line.xpath('./strong/text()').extract_first()
                    sub_posts[-1]['sub_content'] = []
                else:
                    sub_posts[-1]['sub_content'].append(line.xpath('./text()').extract_first())
                    # print(line.xpath('/text()').extract())
            post = Post(title=title, content=sub_posts)
            yield post


        # 队列添加url
        pages = response.xpath('//ul[@class="li_line"]/li//a/@href').extract()
        for page in pages:
            if 'sscx' in page:
                # 选择 'sscx' 类的文章
                page = response.urljoin(page)
                yield scrapy.Request(page, callback=self.parse)



