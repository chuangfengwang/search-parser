# -*- coding: UTF-8 -*-
import json
import html

import traceback
import unittest

from google_parser.exceptions import GoogleParserError, NoBodyInResponseError
from google_parser.tests import GoogleParserTests
from google_parser.google import GoogleParser, SnippetsParserDefault
from google_query import GoogleQuery


class GoogleParserTestCase(GoogleParserTests):
    def test1(self):
        u""""
            一般查询 第一页
            检查下一页,上一页,页数
        """
        query = '人工智能'
        pdf_only = False
        time_select = 'Y'

        if pdf_only:
            query += ' filetype:pdf'
        query_url = GoogleQuery('com', query, time_select).get_url()

        html = self.get_data('1_人工智能-1_2022-08-22.html')
        parser = GoogleParser(html)
        next_page_url = parser.get_next_page_url(query_url)
        previous_page_url = parser.get_previous_page_url(query_url)
        page_num = parser.get_current_page_num()

        # data = {
        #     'query': query,
        #     'query_url': query_url,
        #     'next_page_url': next_page_url,
        #     'previous_page_url': previous_page_url,
        #     'page_num': page_num
        # }
        # print(json.dumps(data, ensure_ascii=False, indent=4))

        self.assertEqual(next_page_url,
                         "https://www.google.com/search?q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&hl=en&gl=US&gr=US-UT&gcs=NewYork&near=Y&ei=lWQDY6iHM_rt2roPhd-S-AQ&start=10&sa=N&ved=2ahUKEwjopb2sqNr5AhX6tlYBHYWvBE8Q8NMDegQIAhBL")
        self.assertEqual(previous_page_url, "")
        self.assertEqual(page_num, 1)

    def test2(self):
        u""""
            一般查询 第二页
            检查下一页,上一页,页数
        """
        query = '人工智能'
        pdf_only = False
        time_select = 'Y'
        start = 2

        if pdf_only:
            query += ' filetype:pdf'
        query_url = GoogleQuery('com', query, time_select, start=start).get_url()

        html = self.get_data('1_人工智能-2_2022-08-22.html')
        parser = GoogleParser(html)
        next_page_url = parser.get_next_page_url(query_url)
        previous_page_url = parser.get_previous_page_url(query_url)
        page_num = parser.get_current_page_num()

        # data = {
        #     'query': query,
        #     'query_url': query_url,
        #     'next_page_url': next_page_url,
        #     'previous_page_url': previous_page_url,
        #     'page_num': page_num
        # }
        # print(json.dumps(data, ensure_ascii=False, indent=4))

        self.assertEqual(next_page_url,
                         "https://www.google.com/search?q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&hl=en&gl=US&gr=US-UT&gcs=NewYork&near=Y&ei=NGoDY6jHMra22roPtp2P-AQ&start=20&sa=N&ved=2ahUKEwiosdLardr5AhU2m1YBHbbOA084ChDw0wN6BAgBEEw")
        self.assertEqual(previous_page_url,
                         "https://www.google.com/search?q=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&hl=en&gl=US&gr=US-UT&gcs=NewYork&near=Y&ei=NGoDY6jHMra22roPtp2P-AQ&start=0&sa=N&ved=2ahUKEwiosdLardr5AhU2m1YBHbbOA084ChDx0wN6BAgBEDc")
        self.assertEqual(page_num, 2)

    def test3(self):
        html = self.get_data('1_人工智能-1_2022-08-22.html')
        parser = GoogleParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'h', 'vu', 'type', 'time'))
        # parser = GoogleParser(html, snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'vu', 'type', 'time'))
        try:
            snippets = parser.get_snippets()
        except Exception as e:
            traceback.print_exc()
        print(json.dumps(snippets, ensure_ascii=False, indent=4))
        self.assertEqual(len(snippets), 9)
        for snippet in snippets:
            self.assertTrue(snippet.get('p'))
            self.assertTrue(snippet.get('u'))
            self.assertTrue(snippet.get('d'))
            self.assertTrue(snippet.get('t'))
            self.assertTrue(snippet.get('s'))
            self.assertTrue(snippet.get('h'))
            self.assertTrue(snippet.get('type'))

    def print_sn(self, snippets):
        for i in snippets:
            print()
            print(i.get('p'))
            print(i.get('u'))
            print(i.get('d'))
            print(i.get('m'))
            print(i.get('t'))
            print(i.get('s'))
            print(i.get('h'))
            print(i.get('uv'))
            print(i.get('type'))
            print(i.get('time'))


if __name__ == '__main__':
    unittest.main()
