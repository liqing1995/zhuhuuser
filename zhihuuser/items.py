# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    headline = Field()
    url = Field()
    avatar_url = Field()
    avatar_url_template = Field()
    url_token = Field()
    user_type = Field()
    type = Field()

    is_advertiser = Field()
    is_followed = Field()
    is_following = Field()
    is_org = Field()

    gender = Field()
    follower_count = Field()
    badge = Field()
    articles_count = Field()
    answer_count = Field()