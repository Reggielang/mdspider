import scrapy
from scrapy.http import Request
import re

from mdspider.items import MdItem


class MdcardsSpider(scrapy.Spider):
    name = "mdcards"
    allowed_domains = ["www.qi-wmcard.com"]
    base_url = f"http://www.qi-wmcard.com"

    # 单独设置MongoDB的pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            "mdspider.pipelines.MongoCardsPipeline": 301,
        },
        #     'DOWNLOADER_MIDDLEWARES':{
        #     'scrapy_proxies.RandomProxy': 100,
        #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        # },
        'SPIDER_MIDDLEWARES': {
            'mdspider.middlewares.CookieMiddleware': 543,
        }
    }

    def __init__(self, *args, **kwargs):
        super(MdcardsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        nums = 5
        for num in range(1, nums):
            parms = f'/series/page/{num}'
            yield Request(
                    url=self.base_url+parms.format(num),
                    callback=self.parse_index,
                    dont_filter=True,
                    priority=0
                )
        # #测试
        # yield Request(
        #         url="http://www.qi-wmcard.com/series/page/1",
        #         callback=self.parse_index,
        #         dont_filter=True,
        #         priority=0
        #     )


    def parse_index(self, response):
        details_indexs = response.xpath('//div[@class="normal-text"]/table[3]//a/@href').getall()

        for card_url in details_indexs:
            card_url = self.base_url + card_url
            yield Request(
                url=card_url,
                callback=self.parse_card_index,
                dont_filter=True,
                priority=0
            )

    def parse_card_index(self, response):
        cards_indexs = response.xpath('//div[@class="normal-text"]/table[3]//a/@href').getall()
        for card_url in cards_indexs:
            card_url = self.base_url + card_url

            #假设每个页面有4个分页
            nums = 15
            for num in range(1, nums):
                parms = f'page/{num}'
                yield Request(
                    url=card_url+parms.format(num),
                    callback=self.parse_card_detail,
                    dont_filter=True,
                    priority=0
                )

    def parse_card_detail(self, response):
        matches = response.xpath('//div[@class="normal-text"]/table[5]/tr/td/table//a/@href').getall()

        unique_matches = set([i for i in matches if 'card' in i])
        for card_detail in unique_matches:
            card_detail_url = self.base_url + card_detail
            yield Request(
                url=card_detail_url,
                callback=self.parse_cards,
                dont_filter=True,
                priority=0
            )

    def parse_cards(self, response):
        item = MdItem()
        table = response.xpath('//td[@class="normal-text"]/table[3]')

        item['ch_name'] = table.xpath('.//tr[td/span[contains(text(), "中文名称")]]/td[2]/text()').get(
            default='N/A').strip()
        item['eng_name'] = table.xpath('.//tr[td/span[contains(text(), "英文名称")]]/td[2]/text()').get(
            default='N/A').strip()
        item['jp_name'] = table.xpath('.//tr[td/span[contains(text(), "日文名称")]]/td[2]/text()').get(
            default='N/A').strip()
        item['card_number'] = table.xpath('.//tr[td/span[contains(text(), "卡片编号")]]/td[2]/text()').get(
            default='N/A').strip()
        item['card_type'] = table.xpath('.//tr[td/span[contains(text(), "卡片种类")]]/td[2]/text()').get(
            default='N/A').strip()
        item['attribute'] = table.xpath('.//tr[td/span[contains(text(), "属性")]]/td[2]/text()').get(
            default='N/A').strip()
        item['race'] = table.xpath('.//tr[td/span[contains(text(), "种族")]]/td[2]/text()').get(default='N/A').strip()
        item['stars'] = table.xpath('.//tr[td/span[contains(text(), "星")]]/td[2]/text()').get(default='N/A').strip()
        item['attack'] = table.xpath('.//tr[td/span[contains(text(), "攻击力")]]/td[2]/text()').get(
            default='N/A').strip()
        item['defence'] = table.xpath('.//tr[td/span[contains(text(), "防御力")]]/td[4]/text()').get(
            default='N/A').strip()
        item['rarity'] = table.xpath('.//tr[td/span[contains(text(), "稀有度")]]/td[2]/text()').get(
            default='N/A').strip()

        desc_tmp = table.xpath('//tr[3]/td/table/tr/td/text()').getall()
        desc = ''.join(i.strip() for i in desc_tmp)
        item['desc'] = desc
        item['img_url'] = self.base_url + table.xpath('.//tr/td/table/tr[2]/td/img/@src').get()

        yield item
