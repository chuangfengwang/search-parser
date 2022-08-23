# -*- coding: UTF-8 -*-
"""
## google parser get_snippets() 结果字段含义
return {
    'p': position,                         # 页面内第几个
    'u': url,                              # 结果的 url
    'd': self._get_domain(url),            # 结果的域名
    'm': self._is_map_snippet(url),        # 是不是地图类结果
    't': self._get_title(title),           # 结果的标题
    's': self._get_descr(snippet, url),    # 结果的描述文本
    'h': self._get_html(snippet),          # 结果的 html
    'vu': self._get_vu(snippet),           # 面包屑导航
    'type': _get_type(snippet),            # 结果类型: PDF,URL
    'time': _get_type(time),               # 结果也中显示的发布时间
}
"""

import re
import unicodedata
from urllib.parse import quote, unquote
from urllib.parse import urlparse, urlunsplit, urlsplit, urljoin

from pyquery import PyQuery
from scrapy.selector import Selector

from google_parser.exceptions import SnippetsParserException, GoogleParserError, NoBodyInResponseError


class GoogleParser(object):
    """调试时间: 2022-08-23"""

    def __init__(self, content,
                 snippet_fields=('d', 'p', 'u', 't', 's', 'm', 'h', 'vu', 'type', 'time')):
        self.content = content
        self.snippet_fields = snippet_fields

    def get_next_page_url(self, page_url):
        """下一页 url"""
        selector = Selector(text=self.content)
        next_a = selector.css('#pnnext::attr(href)').get()
        if next_a:
            next_url = urljoin(page_url, next_a)
            return next_url
        else:
            return ''

    def get_previous_page_url(self, page_url):
        """前一页 url"""
        selector = Selector(text=self.content)
        next_a = selector.css('#pnprev::attr(href)').get()
        if next_a:
            previous_url = urljoin(page_url, next_a)
            return previous_url
        else:
            return ''

    def get_current_page_num(self):
        """当前结果是第几页"""
        selector = Selector(text=self.content)
        page_num = selector.css('.YyVfkd::text').get()
        if page_num:
            return int(page_num)
        else:
            return 1

    def is_suspicious_traffic(self):
        """流量异常"""
        patterns = [
            re.compile(
                r'系统检测到您的计算机网络发出了异常流量', re.I | re.M | re.S
            ),
            re.compile(
                r'<a href="//support\.google\.com/websearch/answer/86640">.*?\.\.\.</a>', re.I | re.M | re.S
            ),
            re.compile(
                r'<p>Your client does not have permission to get URL', re.I | re.M | re.S
            ),
        ]
        result = False
        for pattern in patterns:
            result |= bool(pattern.search(self.content))
            if result:
                break
        return result

    def get_snippets(self):
        """解析结果片段"""
        # 检查正文部分是否存在
        selector = Selector(text=self.content)
        main_div = selector.css('div.main').get(default=None)
        if main_div is None:
            raise NoBodyInResponseError('no body in response')

        # 按条件选择对应的片段解析器
        if Selector(text=self.content).css('div.GLcBOb').get(default=None) is not None:
            return SnippetsParserDefault(self.snippet_fields).get_snippets(self.content)
        else:
            raise GoogleParserError('not found parser version')


class SnippetsParserDefault(object):
    """调试时间: 2022-08-23"""
    snippets_regexp = re.compile(r'(<div class="g">.*?</div><!--n--></div>)', re.I | re.M | re.S)

    def __init__(self, snippet_fields):
        self.snippet_fields = snippet_fields

    def get_snippets(self, body):
        body_list = []
        body_selector = Selector(text=body)
        main_div = body_selector.css('div.main').getall()
        if len(main_div) == 0:
            raise NoBodyInResponseError('no body in response')
        else:
            for body_div in main_div:
                body_list.append(str(body_div))

        result = []
        position = 0
        for body_html in body_list:
            snippet_selector = Selector(text=body_html)
            snippets = snippet_selector.css('div.g').getall()
            snippets = [str(snippet) for snippet in snippets]

            for snippet in snippets:
                position += 1
                try:
                    item = self.get_snippet(position, snippet)
                except SnippetsParserException:
                    if self._is_empty_snippet(snippet):
                        position -= 1
                        continue
                    else:
                        raise

                # игнорим сниппет с картинками
                if self._is_map_snippet(item['u']) or item['u'].startswith('/search'):
                    position -= 1
                    continue

                result.append(item)
        return result

    def get_snippet(self, position, snippet):
        title, url = self._parse_title_snippet(snippet, position)
        return {
            'p': position,
            'u': url,
            'd': self._get_domain(url),
            'm': self._is_map_snippet(url),
            't': self._get_title(title),
            's': self._get_descr(snippet, url),
            'h': self._get_html(snippet),
            'vu': self._get_vu(snippet),
            'type': self._get_type(snippet),
            'time': self._get_time(snippet),
        }

    def _is_empty_snippet(self, snippet):
        return '<h3 class="r"></h3>' in snippet

    @classmethod
    def strip_tags(cls, html):
        return re.sub(r' {2,}', ' ', re.sub(r'<[^>]*?>', '', html.replace('&nbsp;', ' '))).strip()

    @classmethod
    def normalize(cls, url, charset='utf-8'):
        def _clean(string):
            return unicodedata.normalize('NFC', string).encode('utf-8')

        default_port = {
            'ftp': 21,
            'telnet': 23,
            'http': 80,
            'gopher': 70,
            'news': 119,
            'nntp': 119,
            'prospero': 191,
            'https': 443,
            'snews': 563,
            'snntp': 563,
        }

        if url[0] not in ['/', '-'] and ':' not in url[:7]:
            url = 'http://' + url

        url = url.replace('#!', '?_escaped_fragment_=')

        scheme, auth, path, query, fragment = urlsplit(url.strip())
        (userinfo, host, port) = re.search('([^@]*@)?([^:]*):?(.*)', auth).groups()

        scheme = scheme.lower()

        host = host.lower()
        if host and host[-1] == '.':
            host = host[:-1]
            # take care about IDN domains

        path = quote(_clean(path), "~:/?#[]@!$&'()*+,;=")
        fragment = quote(_clean(fragment), "~")

        query = "&".join(
            ["=".join([quote(_clean(t), "~:/?#[]@!$'()*+,;=") for t in q.split("=", 1)]) for q in query.split("&")])

        if scheme in ["", "http", "https", "ftp", "file"]:
            output = []
            part = None
            for part in path.split('/'):
                if part == "":
                    if not output:
                        output.append(part)
                elif part == ".":
                    pass
                elif part == "..":
                    if len(output) > 1:
                        output.pop()
                else:
                    output.append(part)
            if part in ["", ".", ".."]:
                output.append("")
            path = '/'.join(output)

        if userinfo in ["@", ":@"]:
            userinfo = ""

        if path == "" and scheme in ["http", "https", "ftp", "file"]:
            path = "/"

        if port and scheme in default_port.keys():
            if port.isdigit():
                port = str(int(port))
                if int(port) == default_port[scheme]:
                    port = ''

        auth = (userinfo or "") + host
        if port:
            auth += ":" + port
        if url.endswith("#") and query == "" and fragment == "":
            path += "#"
        return urlunsplit((scheme, auth, path, query, fragment))

    @classmethod
    def get_absolute_url(cls, url):
        return cls.normalize(url).replace('//www.', '//')

    @classmethod
    def get_full_domain_without_scheme(cls, url):
        parsed = urlparse(cls.get_absolute_url(url))
        domain = re.sub(r':.+', '', parsed.netloc)
        return urlunsplit(('', domain, '', '', '')).replace('//', '')

    @classmethod
    def format_link(cls, link):
        """提取结果里的 url"""
        link = link.replace('&amp;', '&')

        patterns = [
            r'/interstitial\?url=([^&]*)',
            r'/url\?q=([^&]*)',
            r'/url\?url=([^&]*)',
            r'/infected\?url=([^&]*)',
        ]

        for pattern in patterns:
            res = re.compile(pattern).search(unquote(link))
            if res:
                return res.group(1)
        return link

    def _parse_title_snippet(self, snippet, position):
        """解析结果里的标题和 url """
        snippet = re.sub(r'<div class="action-menu.*?</div>', '', snippet, flags=re.I | re.M | re.S)
        res = re.compile(r'<(?:h3|div)(?: class="r")?[^>]+?>.*?<a[^>]+?href="([^"]+?)"[^>]*?>(.*?)</a>',
                         re.I | re.M | re.S).search(snippet)
        if res:
            title = res.group(2)
            if '<cite' in title:
                title = re.sub(r'<cite.*?</cite>', '', title)

            if title.startswith('<div'):
                title_res = re.search(r'<h3[^>]*?>\s*(?:<div[^>]*?>)(.*?)(?:</div>)</h3>', title,
                                      flags=re.I | re.M | re.S)
                if title_res:
                    title = title_res.group(1)

            return SnippetsParserDefault.strip_tags(title), SnippetsParserDefault.format_link(res.group(1)),
        raise SnippetsParserException(u'Parsing error. Broken snippet at {0}: {1}'.format(position, snippet))

    def _get_domain(self, url):
        """结果的域名"""
        try:
            return self.get_full_domain_without_scheme(url)
        except UnicodeError as e:
            raise GoogleParserError('网址不正确: {0}'.format(url))

    def _is_map_snippet(self, url):
        """是不是地图类型"""
        return 'maps.google' in url

    def _get_title(self, title):
        """结果的标题"""
        if 't' in self.snippet_fields:
            return title

    def _is_image_snippet(self, url):
        """url 是不是图片类型"""
        return url.startswith('/images?q=')

    def _parse_description_img_snippet(self, snippet):
        """搜索结果里的图片描述"""
        res = re.compile(r'<div>(.*?)</div>', re.I | re.M | re.S).search(snippet)
        if res:
            return SnippetsParserDefault.strip_tags(res.group(1))
        raise GoogleParserError(u'找不到 Snippet 的图片描述: {}'.format(snippet))

    def _parse_description_snippet(self, snippet):
        """搜索结果里的文本描述"""
        dom = PyQuery(snippet)
        aim_text = dom('.VwiC3b').text()
        return SnippetsParserDefault.strip_tags(aim_text)

    def _get_descr(self, snippet, url):
        """结果的文本描述"""
        if 's' in self.snippet_fields:
            if self._is_image_snippet(url):
                return self._parse_description_img_snippet(snippet)
            else:
                return self._parse_description_snippet(snippet)

    def _get_html(self, snippet):
        """结果片段的 html"""
        if 'h' in self.snippet_fields:
            return snippet

    def _get_vu(self, snippet):
        """面包屑导航"""
        dom = PyQuery(snippet)
        aim_text = dom('a cite.iUh30').text()
        return SnippetsParserDefault.strip_tags(aim_text)

    def _get_type(self, snippet):
        """结果类型: PDF, URL"""
        dom = PyQuery(snippet)
        aim_text = dom('.ZGwO7.C0kchf.NaCKVc.VDgVie').text()
        if aim_text:
            return SnippetsParserDefault.strip_tags(aim_text)
        else:
            return 'URL'

    def _get_time(self, snippet):
        """结果中标注的发布时间"""
        dom = PyQuery(snippet)
        aim_text = dom('.MUxGbd.wuQ4Ob.WZ8Tjf').text()
        text = SnippetsParserDefault.strip_tags(aim_text).strip().strip('—')
        return text
