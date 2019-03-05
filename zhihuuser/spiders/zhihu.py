# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Spider, Request

from zhihuuser.items import UserItem


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_quert = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_quert = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_quert = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_quert), self.parse_user)

        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_quert, offset=0, limit=20),
                      self.parse_follows)

        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_quert, offset=0, limit=20),
                      self.parse_followers)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)  # 进行赋值
        yield item

        yield Request(
            self.follows_url.format(user=result.get('url_token'), include=self.follows_quert, offset=0, limit=20),
            self.parse_follows)

        yield Request(
            self.followers_url.format(user=result.get('url_tokken'), include=self.followers_quert, offset=0, limit=20),
            self.parse_followers)

    def parse_follows(self, response):
        result = json.loads(response.text)

        if 'data' in result.keys():
            for result in result.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_quert),
                              self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_pagge = result.get('paging').get('next')
            yield Request(next_pagge, self.parse_follows)  # 回调自己

    def parse_followers(self, response):
        result = json.loads(response.text)

        if 'data' in result.keys():
            for result in result.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'), include=self.user_quert),
                              self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_pagge = result.get('paging').get('next')
            yield Request(next_pagge, self.parse_followers)  # 回调自己
