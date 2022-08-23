### 项目介绍

一个用于解析搜索引擎结果页面的 python 库, 仅支持 python3.

目前仅支持 google 搜索结果解析

### google-parser 使用方式

```python
import json
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

print(json.dumps(snippets, ensure_ascii=False, indent=4))

# 获取下一页
html_next_page = splash_agent.get_html(next_page_url)

```

json 结果样例如下

```json
[
  {
    "p": 1,
    "u": "https://zh.m.wikipedia.org/zh-hant/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD",
    "d": "zh.m.wikipedia.org",
    "m": false,
    "t": "人工智能- 维基百科，自由的百科全书",
    "s": "人工智能可以定義為模仿人類與人類思維相關的認知功能的機器或計算機，如學習和解決問題。人工智能是計算機科學的一個分支，它感知其環境並採取行動，最大限度地提高其成功 ... 人工智慧(AI) 是透過建立及應用內建於動態運算環境中的演算法，來模擬人類智慧過程的基礎。簡言之， AI 的目標是試圖讓電腦像人類一樣思考和行動。 實現這項目標需要三個 ... 人工智能（Artificial Intelligence），英文縮寫為AI。它是研究、開發用於模擬、延伸和擴展人的智能的理論、方法、技術及應用系統的一門新的技術科學。人工智能是 ... 简单来说，人工智能(AI) 是指可模仿人类智能来执行任务，并基于收集的信息对自身进行迭代式改进的系统和机器。AI 具有多种形式。例如： ... AI 更多的是一种为超级思考和数据 ... 人工智能(AI) 是致力于解决通常与人工智能相关联的认知性问题的计算机科学领域，这些问题包括学习、问题解决和模式识别等。提起人工智能（通常缩写为“AI”），人们可能 ... 从广义上来说，人工智能(AI) 是指机器或系统所呈现的任何模拟人类的行为。最基本的AI 形式是对计算机进行编程，使它们能够根据从过去类似行为中收集的海量数据来“模拟” ... 人工智能(AI) 让机器可以从经验中学习，适应新的输入并像人一样完成任务。您今天所听说到的大多数AI 示例–从下国际象棋的计算机到自动驾驶汽车–都十分依赖深度学习和 ... 現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://zh.m.wikipedia.org › zh-hant https://www.netapp.com › zh-hant https://baike.baidu.hk › item › 人工... https://www.oracle.com › what-is-ai https://aws.amazon.com › what-is-ai https://www.hpe.com › what-is › artif... https://www.sas.com › ... › 分析 https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 2,
    "u": "https://www.netapp.com/zh-hant/artificial-intelligence/what-is-artificial-intelligence/",
    "d": "netapp.com",
    "m": false,
    "t": "什麼是人工智慧（即AI）？為什麼人工智慧很重要 - NetApp",
    "s": "人工智慧(AI) 是透過建立及應用內建於動態運算環境中的演算法，來模擬人類智慧過程的基礎。簡言之， AI 的目標是試圖讓電腦像人類一樣思考和行動。 實現這項目標需要三個 ... 人工智能（Artificial Intelligence），英文縮寫為AI。它是研究、開發用於模擬、延伸和擴展人的智能的理論、方法、技術及應用系統的一門新的技術科學。人工智能是 ... 简单来说，人工智能(AI) 是指可模仿人类智能来执行任务，并基于收集的信息对自身进行迭代式改进的系统和机器。AI 具有多种形式。例如： ... AI 更多的是一种为超级思考和数据 ... 人工智能(AI) 是致力于解决通常与人工智能相关联的认知性问题的计算机科学领域，这些问题包括学习、问题解决和模式识别等。提起人工智能（通常缩写为“AI”），人们可能 ... 从广义上来说，人工智能(AI) 是指机器或系统所呈现的任何模拟人类的行为。最基本的AI 形式是对计算机进行编程，使它们能够根据从过去类似行为中收集的海量数据来“模拟” ... 人工智能(AI) 让机器可以从经验中学习，适应新的输入并像人一样完成任务。您今天所听说到的大多数AI 示例–从下国际象棋的计算机到自动驾驶汽车–都十分依赖深度学习和 ... 現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://www.netapp.com › zh-hant https://baike.baidu.hk › item › 人工... https://www.oracle.com › what-is-ai https://aws.amazon.com › what-is-ai https://www.hpe.com › what-is › artif... https://www.sas.com › ... › 分析 https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 3,
    "u": "https://baike.baidu.hk/item/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/9180",
    "d": "baike.baidu.hk",
    "m": false,
    "t": "人工智能_百度百科",
    "s": "人工智能（Artificial Intelligence），英文縮寫為AI。它是研究、開發用於模擬、延伸和擴展人的智能的理論、方法、技術及應用系統的一門新的技術科學。人工智能是 ... 简单来说，人工智能(AI) 是指可模仿人类智能来执行任务，并基于收集的信息对自身进行迭代式改进的系统和机器。AI 具有多种形式。例如： ... AI 更多的是一种为超级思考和数据 ... 人工智能(AI) 是致力于解决通常与人工智能相关联的认知性问题的计算机科学领域，这些问题包括学习、问题解决和模式识别等。提起人工智能（通常缩写为“AI”），人们可能 ... 从广义上来说，人工智能(AI) 是指机器或系统所呈现的任何模拟人类的行为。最基本的AI 形式是对计算机进行编程，使它们能够根据从过去类似行为中收集的海量数据来“模拟” ... 人工智能(AI) 让机器可以从经验中学习，适应新的输入并像人一样完成任务。您今天所听说到的大多数AI 示例–从下国际象棋的计算机到自动驾驶汽车–都十分依赖深度学习和 ... 現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "nonce=\"jvPSXpz-kiNSu-iq-GtKlA\"></script></body></html>\n",
    "vu": "https://baike.baidu.hk › item › 人工... https://www.oracle.com › what-is-ai https://aws.amazon.com › what-is-ai https://www.hpe.com › what-is › artif... https://www.sas.com › ... › 分析 https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 4,
    "u": "https://www.oracle.com/cn/artificial-intelligence/what-is-ai/",
    "d": "oracle.com",
    "m": false,
    "t": "人工智能(AI) 是什么| Oracle 中国",
    "s": "简单来说，人工智能(AI) 是指可模仿人类智能来执行任务，并基于收集的信息对自身进行迭代式改进的系统和机器。AI 具有多种形式。例如： ... AI 更多的是一种为超级思考和数据 ... 人工智能(AI) 是致力于解决通常与人工智能相关联的认知性问题的计算机科学领域，这些问题包括学习、问题解决和模式识别等。提起人工智能（通常缩写为“AI”），人们可能 ... 从广义上来说，人工智能(AI) 是指机器或系统所呈现的任何模拟人类的行为。最基本的AI 形式是对计算机进行编程，使它们能够根据从过去类似行为中收集的海量数据来“模拟” ... 人工智能(AI) 让机器可以从经验中学习，适应新的输入并像人一样完成任务。您今天所听说到的大多数AI 示例–从下国际象棋的计算机到自动驾驶汽车–都十分依赖深度学习和 ... 現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://www.oracle.com › what-is-ai https://aws.amazon.com › what-is-ai https://www.hpe.com › what-is › artif... https://www.sas.com › ... › 分析 https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 5,
    "u": "https://aws.amazon.com/cn/machine-learning/what-is-ai/",
    "d": "aws.amazon.com",
    "m": false,
    "t": "什么是人工智能？_深度学习是什么？ - AWS 云服务",
    "s": "人工智能(AI) 是致力于解决通常与人工智能相关联的认知性问题的计算机科学领域，这些问题包括学习、问题解决和模式识别等。提起人工智能（通常缩写为“AI”），人们可能 ... 从广义上来说，人工智能(AI) 是指机器或系统所呈现的任何模拟人类的行为。最基本的AI 形式是对计算机进行编程，使它们能够根据从过去类似行为中收集的海量数据来“模拟” ... 人工智能(AI) 让机器可以从经验中学习，适应新的输入并像人一样完成任务。您今天所听说到的大多数AI 示例–从下国际象棋的计算机到自动驾驶汽车–都十分依赖深度学习和 ... 現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://aws.amazon.com › what-is-ai https://www.hpe.com › what-is › artif... https://www.sas.com › ... › 分析 https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 6,
    "u": "https://www.hpe.com/cn/zh/what-is/artificial-intelligence.html",
    "d": "hpe.com",
    "m": false,
    "t": "什么是人工智能(AI)？ | 词汇表| 慧与",
    "s": "从广义上来说，人工智能(AI) 是指机器或系统所呈现的任何模拟人类的行为。最基本的AI 形式是对计算机进行编程，使它们能够根据从过去类似行为中收集的海量数据来“模拟” ... 人工智能(AI) 让机器可以从经验中学习，适应新的输入并像人一样完成任务。您今天所听说到的大多数AI 示例–从下国际象棋的计算机到自动驾驶汽车–都十分依赖深度学习和 ... 現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://www.hpe.com › what-is › artif... https://www.sas.com › ... › 分析 https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 7,
    "u": "https://www.sas.com/zh_cn/insights/analytics/what-is-artificial-intelligence.html",
    "d": "sas.com",
    "m": false,
    "t": "人工智能–它是什么，它为什么重要 - SAS",
    "s": "人工智能(AI) 让机器可以从经验中学习，适应新的输入并像人一样完成任务。您今天所听说到的大多数AI 示例–从下国际象棋的计算机到自动驾驶汽车–都十分依赖深度学习和 ... 現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://www.sas.com › ... › 分析 https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 8,
    "u": "https://www.trendmicro.com/zh_hk/what-is/machine-learning/artificial-intelligence.html",
    "d": "trendmicro.com",
    "m": false,
    "t": "甚麼是人工智能？ - Trend Micro",
    "s": "現時有兩個主要方法利用電腦、機器、程式及源碼的決策及解決問題能力來模擬人類思維與本能，包括人性化方法及理想化方法。 人工智能; 人性化方法; 理性方法 ... Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://www.trendmicro.com › what-is https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  },
  {
    "p": 9,
    "u": "https://easyai.tech/ai-definition/ai/",
    "d": "easyai.tech",
    "m": false,
    "t": "「2021更新」一文看懂人工智能- AI",
    "s": "Dec 28, 2018 — 人工智能（Artificial Intelligence），英文缩写为AI。它是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "h": "<div class= <very long html text>\n",
    "vu": "https://easyai.tech › ai-definition",
    "type": "URL",
    "time": "Dec 28, 2018 "
  }
]
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

### known bugs

- 切分 snippet 结果不正确, 并导致了后面的错误
- s 结果包含内容过多
- vu 结果包含内容过多
- time 结果是页面内任何一个有效时间

### 致谢

本项目简化了这个的项目, 且部分数据和代码来源于此, 并适配了 python3: [google-parser](https://github.com/KokocGroup/google-parser)
