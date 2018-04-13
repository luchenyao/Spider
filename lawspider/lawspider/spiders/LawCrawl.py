# coding=utf=8
# Author: LuChenyao
# Date:2018-03-26


import scrapy

class VocItem(scrapy.Item):
    title=scrapy.Field()
    content = scrapy.Field()

class LawSpider(scrapy.Spider):
    name = 'voc'
    start_urls = ["http://baike.baidu.com/"]

    def start_requests(self):
        urls = [
            'http://baike.baidu.com/fenlei/%E6%B3%95%E5%BE%8B',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            category = response.xpath('//div[@class="category-title "]')
            if category:
                # 如果是词条列表， 则将词条、分类的翻页、子分类加入队列
                """当前分类下的词条加入队列"""
                item_list = response.xpath('//div[@class="grid-list grid-list-spot"]//div[@class="list"]/a/@href').extract()
                for item_url in item_list:
                    if '/view/' in item_url:
                        yield scrapy.Request('http://baike.baidu.com' + item_url, callback=self.parse)

                ############################################
                # 这段内容调试单个页面的时候建议注释关掉
                # Begin

                """当前分类的翻页加入队列"""
                indexs = response.xpath('//div[@id="pageIndex"]/a/@href').extract()
                for url in indexs:
                    yield scrapy.Request('http://baike.baidu.com/fenlei/' + url, callback=self.parse)

                """将子分类的url加入队列"""
                sub_urls = category.xpath('./a/@href').extract()
                for url in sub_urls:
                    yield scrapy.Request('http://baike.baidu.com' + url, callback=self.parse)
                    # End
                    ############################################

            else:
                # 如果是词条，处理词条内容，抓取需要的内容
                ############################################
                """TODO"""

                law_dict=[]
                title=response.xpath('//div[@class="main-content"]/dl[@class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-"]/dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()').extract()
                title=''.join(title).strip()
                voc_def=response.xpath('//div[@class="main-content"]/div[@class="lemma-summary"]/div[@class="para"]/text()').extract()
                if voc_def:
                    voc_def=''.join(voc_def).strip()
                    voc_def=voc_def.replace("\n","")
                else:
                    # voc_def = response.xpath('//div[@class="lemma-summary"]//text()')
                    # if
                    voc_def=response.xpath('//div[@class="lemma-summary"]//text()').extract()
                    voc_def = ''.join(voc_def).strip()
                    voc_def=voc_def.replace("\n","")
                law_dict.append({'fir_class_title':'定义','description':voc_def})

                t = response.xpath(
                    './/div[@class="main-content"]/div[@class="para-title level-2"] | .//div[@class="main-content"]/div[@class="para-title level-3"] | .//div[@class="main-content"]/div[@class="para"]')
                if t:
                    for each in t:
                        if each.xpath('./@class').extract_first()=="para-title level-2":
                            fir_title=each.xpath('./h2[@class="title-text"]/text()').extract()
                            fir_title=''.join(fir_title).strip()
                            fir_title=fir_title.replace("\n","")
                            if fir_title:
                                law_dict.append({'fir_class_title':fir_title,'description':[]})

                        if each.xpath('./@class').extract_first()=="para-title level-3":
                            sec_title=each.xpath('./h3[@class="title-text"]/text()').extract()
                            sec_title=''.join(sec_title).strip()
                            sec_title=sec_title.replace("\n","")
                            if sec_title:
                                law_dict[-1]['description'].append({'sec_class_title':sec_title,'para':[]})

                        if each.xpath('./@class').extract_first()=="para":
                            para=each.xpath('.//text()').extract()
                            para=''.join(para).strip()
                            para=para.replace("\n","")
                            if para:
                                if len(law_dict[-1]['description'])==0:
                                    law_dict[-1]['description'].append(para)
                                else:
                                    if isinstance(law_dict[-1]['description'][-1],str):
                                        law_dict[-1]['description'].append(para)
                                    if isinstance(law_dict[-1]['description'][-1],dict):
                                        law_dict[-1]['description'][-1]['para'].append(para)

                yield VocItem(title=title,content=law_dict)
                pass

        except:
            print("##############################################")
            print("error")
            print("##############################################")
