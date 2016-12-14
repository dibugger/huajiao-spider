# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class StackItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()

class UserItem(scrapy.Item):
    avatar = scrapy.Field()
    user_id = scrapy.Field()
    followings = scrapy.Field()
    followers = scrapy.Field()
    likes = scrapy.Field()
    experience = scrapy.Field()
