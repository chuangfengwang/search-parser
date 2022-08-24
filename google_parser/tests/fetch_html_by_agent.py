# -*- coding: UTF-8 -*-
import datetime

from google_parser.tests import GoogleParserTests
from common import SplashAgent
from google_query import GoogleQuery

# 代理地址配置
splash_html_url = 'http://192.168.0.107:8050/render.html'
splash_json_url = 'http://192.168.0.107:8050/render.json'
splash_execute_url = 'http://192.168.0.107:8050/execute'
splash_proxy = 'http://192.168.0.107:8118'

# splash 代理
splash_agent = SplashAgent(splash_html_url, splash_proxy)


def gen_datetime_postfix():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def fetch_htm_by_splash(url: str, file_name: str):
    """通过 splash 代理获取 html"""
    html = splash_agent.get_html(url)
    test = GoogleParserTests()
    test.write_data(file_name, html)
    return html


def test1():
    """从搜索词生成页面 html 文件"""
    query = '第四范式招股书'
    pdf_only = False
    time_select = 'Y'

    if pdf_only:
        query += ' filetype:pdf'
    query_url = GoogleQuery('com', query, time_select).get_url()

    _ = fetch_htm_by_splash(query_url, '1_第四范式招股书-1_{}.html'.format(gen_datetime_postfix()))


def test2():
    """从 url 生成页面 html 文件"""
    query_url = 'https://www.google.com/search?q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&hl=en&gl=US&gr=US-UT&gcs=NewYork&near=Y&ei=lWQDY6iHM_rt2roPhd-S-AQ&start=10&sa=N&ved=2ahUKEwjopb2sqNr5AhX6tlYBHYWvBE8Q8NMDegQIAhBL'
    _ = fetch_htm_by_splash(query_url, '1_人工智能-2_{}.html'.format(gen_datetime_postfix()))


if __name__ == '__main__':
    test1()
    # test2()
    pass
