#-*- coding:utf-8 -*-
import json
import os
from mitmproxy.http import HTTPFlow


class DouYuHandler:
    """
    用于mitmdump的斗鱼数据抓包处理程序
    抓取连接中的直播rtmp地址
    """
    def get_rtmp_url(self, data: str) -> str:
        data = json.loads(data)['data']
        rtmp_live = data['rtmp_live']
        rtmp_url = data['rtmp_url'].replace('\\', '')
        return '{}/{}'.format(rtmp_url, rtmp_live)

    def handle_request(self, flow: HTTPFlow) -> HTTPFlow:
        pass

    def handle_response(self, flow: HTTPFlow) -> HTTPFlow:
        req = flow.request
        rsp = flow.response
        if req.url.find('getH5Play') != -1:
            rtmp_url = self.get_rtmp_url(rsp.text)
            with open(os.path.join('/tmp', 'rtmp.dat'), 'w', encoding='utf-8') as f:
                f.write(rtmp_url)
                f.flush()


class LiveHandler:
    """
    总处理
    """
    def __init__(self, *handler):
        self.handlers = [handle for handle in handler]

    def requerst(self, flow: HTTPFlow):
        for handler in self.handlers:
            handler.handle_request(flow)

    def response(self, flow: HTTPFlow):
        for handler in self.handlers:
            handler.handle_response(flow)


addons = [
    LiveHandler(DouYuHandler())
]