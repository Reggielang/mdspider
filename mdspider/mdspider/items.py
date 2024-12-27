# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ch_name = scrapy.Field()  # 中文名称
    eng_name = scrapy.Field()  # 英文名称
    jp_name = scrapy.Field()  # 日文名称
    card_number = scrapy.Field()  # 卡片编号
    card_type = scrapy.Field()  # 卡片种类
    attribute = scrapy.Field()  # 属性
    race = scrapy.Field()  # 种族
    stars = scrapy.Field()  # 星级
    attack = scrapy.Field()  # 攻击力
    defence = scrapy.Field()  # 防御力
    rarity = scrapy.Field()  # 稀有度
    desc = scrapy.Field()  # 描述（如果有的话）
    img_url = scrapy.Field()