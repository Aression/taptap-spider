#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import pypinyin
import scrapy
from scrapy import FormRequest

from ProjSettings import *
from ..items import GameDetailItem


def _game_raw_info_spider_factory(_name: str = 'GameRawInfoSpider_name_UNDEFINED', category: str = None):
    """
    Factory function to create multiple spiders for each category to get raw infomation.
    """

    class _GameRawInfoSpiderBase(scrapy.Spider):
        name = _name

        def __init__(self):
            super(_GameRawInfoSpiderBase, self).__init__()
            self.category_name = category

            if category is None or self.name == 'GameRawInfoSpider_name_UNDEFINED':
                raise NameError("Spider Name Is Not Properly Initialized")

        def start_requests(self):
            return [FormRequest(
                url=domain + category_details.format(self.category_name, X_UA),
                callback=self.parse,
                headers=headers
            )]

        def parse(self, response, **kwargs):
            try:
                db = json.loads(response.text)
                for i in db['data']['list']:
                    item = GameDetailItem()
                    item['id'] = i['app']['id']
                    yield FormRequest(
                        url=domain + app_details.format(i['app']['id'], X_UA),
                        meta={'item': item},
                        callback=self.parse_game_details,
                        headers=headers
                    )

                if db['data']['next_page'] != '':
                    yield FormRequest(
                        url=f"{db['data']['next_page']}&X-UA={X_UA}",
                        callback=self.parse,
                        headers=headers
                    )
            except Exception as e:
                self.logger.error(
                    f'Get details info failed due to following error: \n{e}')

        def parse_game_details(self, response, **kwargs):
            try:
                db = json.loads(response.text)
                item = response.meta['item']
                item['name'] = db['data']['title']
                if db['data'].__contains__('tags'):
                    item['tags'] = [
                        j['value'] for j in db['data']['tags']
                    ]
                else:
                    item['tags'] = []
                item['companies'] = [
                    {'type': i['type'], 'name': i['name']} for i in db['data']['developers']
                ]
                item['current_price'] = db['data']['price']['taptap_current']
                item['original_price'] = db['data']['price']['taptap_original']
                item['downloads'] = db['data']['stat']['play_total']

                if db['data']['stat'].__contains__('vote_info'):
                    item['vote_info'] = db['data']['stat']['vote_info']
                else:
                    item['vote_info'] = {"1": -1, "2": -
                                         1, "3": -1, "4": -1, "5": -1}

                # don't get reviews
                item['comment'] = []

                yield item
            except Exception as e:
                self.logger.error(
                    f'parse_game_details failed due to following error: \n{e}')

    _GameRawInfoSpiderBase.__name__ = _name
    _GameRawInfoSpiderBase.__qualname__ = _name
    return _GameRawInfoSpiderBase


for tag in tag_icons:
    spider_name = '_'.join(
        [i[0] for i in pypinyin.pinyin(tag, style=pypinyin.NORMAL)])
    globals()[
        f'GameRawInfoSpider_{spider_name}'
    ] = _game_raw_info_spider_factory(f'GameRawInfoSpider_{spider_name}', tag)
