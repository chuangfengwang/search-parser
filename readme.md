### 项目介绍

一个用于解析搜索引擎结果页面的 python 库, 仅支持 python3.

### google-parser 使用方式

```python
from common import SplashAgent
from google_query import GoogleQuery
from google_parser import GoogleParser

# 首先安装 splash; 如有需要, 安装用于访问 google 的网络代理
# 代理地址配置
splash_html_url = 'http://192.168.0.107:8050/render.html'
splash_json_url = 'http://192.168.0.107:8050/render.json'
splash_execute_url = 'http://192.168.0.107:8050/execute'
splash_proxy = 'http://192.168.0.107:8118'  # splash 访问网页使用的代理

# splash 代理
splash_agent = SplashAgent(splash_url=splash_html_url, splash_proxy=splash_proxy)

query = '查询词,搜索框输入的内容'
time_select = 'y'  # '':不设定,'y':过去一年,'m':过去一月,'w':过去一周,'d':过去一天,'h':过去一小时
query_url = GoogleQuery('com', query=query, tbs=time_select).get_url()

html = splash_agent.get_html(query_url)
parser = GoogleParser(html)
snippets = parser.get_snippets()

next_page_url = parser.get_next_page_url(query_url)  # 下一页 url
previous_page_url = parser.get_previous_page_url(query_url)  # 上一页 url
page_num = parser.get_current_page_num()  # 当前结果是第几页

for snippet in snippets:
    print(snippet.get('p'))  # 页面内第几个
    print(snippet.get('u'))  # 结果的 url
    print(snippet.get('d'))  # 结果的域名
    print(snippet.get('m'))  # 是不是地图类结果
    print(snippet.get('t'))  # 结果的标题
    print(snippet.get('s'))  # 结果的描述文本
    print(snippet.get('h'))  # 结果的 html
    print(snippet.get('vu'))  # 面包屑导航
    print(snippet.get('type'))  # 结果类型: PDF,URL
    print(snippet.get('time'))  # 结果也中显示的发布时间

# 获取下一页
html_next_page = splash_agent.get_html(next_page_url)

```

### google-parser 结果字段含义

```python
return {
    'p': position,  # 页面内第几个
    'u': url,  # 结果的 url
    'd': cls._get_domain(url),  # 结果的域名
    'm': cls._is_map_snippet(url),  # 是不是地图类结果
    't': cls._get_title(title),  # 结果的标题
    's': cls._get_descr(snippet, url),  # 结果的描述文本
    'h': cls._get_html(snippet),  # 结果的 html
    'vu': cls._get_vu(snippet),  # 面包屑导航
    'type': _get_type(snippet),  # 结果类型: PDF,URL
    'time': _get_type(time),  # 结果也中显示的发布时间
}
```

### 致谢
该项目简化了下面的项目, 并适配了 python3
[google-parser](https://github.com/KokocGroup/google-parser)
