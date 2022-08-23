# -*- coding: UTF-8 -*-

import requests


class SplashAgent:
    """splash代理"""

    def __init__(self, splash_url, splash_proxy=None, splash_html=None, splash_har=None, splash_response_body=None,
                 splash_headers=None):
        self.splash_url = splash_url
        self.splash_proxy = splash_proxy
        self.splash_html = splash_html
        self.splash_har = splash_har
        self.splash_response_body = splash_response_body
        self.splash_headers = splash_headers

        self.session_json_header = {'Content-Type': 'application/json'}
        self.session = requests.Session()
        self.session.headers.update(self.session_json_header)

    def get_html(self, aim_url, extra_params=None):
        param = {
            'url': aim_url,
        }
        if self.splash_proxy is not None:
            param['proxy'] = self.splash_proxy
        if self.splash_headers is not None:
            param['headers'] = self.splash_headers
        if extra_params is not None:
            param.update(extra_params)
        response = self.session.post(url=self.splash_url, json=param)
        return response.text

    def get_json(self, aim_url, extra_params=None):
        param = {
            'url': aim_url,
        }
        if self.splash_proxy is not None:
            param['proxy'] = self.splash_proxy
        if self.splash_html is not None:
            param['html'] = self.splash_html
        if self.splash_har is not None:
            param['har'] = self.splash_har
        if self.splash_response_body is not None:
            param['response_body'] = self.splash_response_body
        if self.splash_headers is not None:
            param['headers'] = self.splash_headers
        if extra_params is not None:
            param.update(extra_params)
        response = self.session.post(url=self.splash_url, json=param)
        return response.text

    def get_execute(self, aim_url, extra_params=None):
        param = {
            'url': aim_url,
        }
        if self.splash_proxy is not None:
            param['proxy'] = self.splash_proxy
        if self.splash_html is not None:
            param['html'] = self.splash_html
        if self.splash_har is not None:
            param['har'] = self.splash_har
        if self.splash_response_body is not None:
            param['response_body'] = self.splash_response_body
        if self.splash_headers is not None:
            param['headers'] = self.splash_headers
        if extra_params is not None:
            param.update(extra_params)
        response = self.session.post(url=self.splash_url, json=param)
        return response.text

    def __del__(self):
        self.session.close()
