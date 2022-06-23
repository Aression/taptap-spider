#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import json
import jsonlines
import pypinyin
import scrapy
from scrapy import FormRequest

from ProjSettings import *
from ..items import GameDetailItem


def _game_details_spider_factory(_name: str = 'GameDetailsSpider_name_UNDEFINED', game_id: str = None):
    """
    Factory function to create multiple spiders for each game
    """

    class _GameDetailsSpiderBase(scrapy.Spider):
        name = _name
        def __init__(self):
            super(_GameDetailsSpiderBase, self).__init__()
            self.game_id = game_id
            self.func_path = domain + app_details.format(self.game_id, X_UA)

        def start_requests(self):
            return [FormRequest(
                url=self.func_path,
                callback=self.parse,
                headers=headers
            )]

        def parse(self, response, **kwargs):
            item = GameDetailItem()
            try:
                # this is not properlly implemented, need to be fixed
                db = json.loads(response.text)
                item['name'] = db['data']['app']['title']
                item['id'] = db['data']['app']['id']
                item['img_url'] = db['data']['app']['icon']['url']
                item['price'] = db['data']['app']['price']
                item['downloads'] = db['data']['app']['play_total']
                item['stat'] = db['data']['app']['stat']['rating']['score']
                item['tags'] = [j['value'] for j in db['data']['app']['tags']]
                yield item
            except Exception as e:
                logging.ERROR(
                    "Error in parsing game details: {}".format(e)
                )
    _GameDetailsSpiderBase.__name__ = _name
    _GameDetailsSpiderBase.__qualname__ = _name
    return _GameDetailsSpiderBase

"""
设计思路：
1. GameDetailsSpider的创建依赖于id，所以只能在GameCategorySpider中创建。
2. 如果把GameDetailsSpider的爬取过程放在GameCategorySpider中，那么就会导致GameCategorySpider的爬取过程中，
   将不同类别的结果存放到一个文件里面。
3. 所以需要在GameCategorySpider中向pipeline传参，指定不同类型数据的写入位置。
"""