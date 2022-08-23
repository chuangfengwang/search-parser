# -*- coding: UTF-8 -*-
import urllib.parse

from .google_query_data import regions, regions_coords


class GoogleQueryError(Exception):
    pass


class GoogleQuery:
    base_url_tpl = 'https://www.google.{zone}/search?q={query}{params}'

    zone_params = {
        'com.ua': {
            'hl': 'ru'
        },
        'co.uk': {
            'hl': 'en'
        },
        'co.id': {
            'hl': 'en',
            'custom': 'gl=en'
        },
        'com.hk': {
            'hl': 'en',
            'custom': 'gl=en&pws=0&gcs=Hongkong'
        },
        'bg': {
            'hl': 'bg'
        },
        'com.uag': {
            'hl': 'ru',
            'custom': 'tbs=ctr:countryUA&cr=countryUA'
        },
        'com': {
            'hl': 'en',
            'custom': 'gl=US&gr=US-UT&gcs=NewYork'
        }
    }

    num = 10

    regions = regions
    regions_coords = regions_coords

    def __init__(self, zone, query, tbs='', region=None, start=0, num=10, zone_params=None, always_params='as_dt=e',
                 custom_params=None):
        """

        :param zone: google 域名后缀. 如: com, com.hk
        :param query: 查询词
        :param tbs: 时间限制. '':不设定,'y':过去一年,'m':过去一月,'w':过去一周,'d':过去一天,'h':过去一小时
        :param region:
        :param start: 第几页
        :param num: 每页多少个
        :param zone_params:
        :param always_params:
        :param custom_params:
        """
        self.zone = zone
        self.query = query
        self.tbs = tbs
        self.region = region
        self.start = int(start) * num
        self.always_params = always_params
        self.num = int(num) if num else self.num
        self.custom_params = custom_params

        if zone_params:
            self.zone_params = zone_params

    @classmethod
    def get_zone_and_region(cls, region):
        if not region:
            raise GoogleQueryError(u'无效区域: {0}'.format(region))

        params = cls.regions.get(region.strip().lower())
        if not params:
            raise GoogleQueryError(u'无效区域: {0}'.format(region))

        return params

    def _get_crutch_zone(self):
        if self.zone == 'com.uag':
            return 'com.ua'
        return self.zone

    @classmethod
    def get_region_cookie(cls, region):
        from base64 import b64encode
        import time

        coords = cls.regions_coords.get(region.lower())
        if not coords:
            return {}

        coords = [coords['latitude'], coords['longitude']]
        n = 'role:1\n' \
            'producer:12\n' \
            'provenance:6\n' \
            'timestamp: {0}\n' \
            'latlng{{\n' \
            'latitude_e7:{1}\n' \
            'longitude_e7:{2}\n' \
            '}}\n' \
            'radius:29140'
        n = n.format(int(time.time()) * 100000, coords[0], coords[1])
        cookie_value = 'a+{0}'.format(b64encode(n.encode(encoding='utf-8')))
        return {'UULE': cookie_value}

    def get_url(self):
        u"""返回 url"""

        params = ''

        if self.num:
            params += '&num={0}'.format(self.num)

        if self.start:
            params += '&start={0}'.format(self.start)

        zone_params = self.zone_params.get(self.zone, {})
        hl = zone_params.get('hl')
        if hl:
            params += '&hl={0}'.format(hl)
        if self.tbs:
            params += '&tbs=qdr:{}'.format(self.tbs)

        zone_custom = zone_params.get('custom', {})
        if zone_custom:
            params += '&{}'.format(zone_custom)

        if self.always_params:
            params += '&{}'.format(self.always_params)

        if self.region:
            params += '&near={0}'.format(urllib.parse.quote(self.region))

        if self.custom_params:
            params += '&{0}'.format(self.custom_params)

        return self.base_url_tpl.format(
            zone=self._get_crutch_zone(), query=urllib.parse.quote(self.query), params=params
        )
