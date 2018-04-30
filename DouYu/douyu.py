#!/usr/bin/python3
#-*- coding:utf-8 -*-
import requests
import json
import os
import argparse
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


class DouYu:
    """
    douyu直播爬虫，爬取直播流
    调用ffmepg下载视频流
    >>>DouYu = DouYu()
    >>>DouYu.get_room_status('24422')
    >>>DouYu.get_room_url('24422')
    """
    def __init__(self, proxy_port: str='8080'):
        self._session = requests.Session()
        self._session.cookies.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})
        self._proxy_port = proxy_port

    def _init_browser(self, proxy: Proxy=None) -> webdriver:
        """
        初始化浏览器代理，指向为proxy的代理端口
        :param proxy: selenium.webdriver.common.proxy.Proxy类型的代理设置
        :return: webdriver
        """
        if not proxy:
            proxy_url = 'localhost:%s' % self._proxy_port
            proxy = Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = proxy_url
            proxy.ssl_proxy = proxy_url
        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)
        return webdriver.Chrome(desired_capabilities=capabilities)

    def get_room_status(self, room_id):
        """
        通过开放api查询直播间状态
        :param room_id: 直播间id或别名
        :return: 如果网络错误或直播间id错误，返回None, 否则返回一个状态字典
        """
        api_url = 'http://open.douyucdn.cn/api/RoomApi/room/%s' % room_id
        try:
            r = self._session.get(api_url)
            r.raise_for_status()
        except ConnectionError as e:
            print('网络错误： ' + e.strerror)
            return None
        except requests.exceptions.HTTPError as e:
            print('请求错误： ' + e.strerror)
            return None
        else:
            return json.loads(r.text)

    def check_is_living(self, room_id: str) -> bool:
        """
        查询直播间是否开播
        :param room_id: 直播间id或别名
        :return: 开播返回True, 否则False
        """
        status = self.get_room_status(room_id)
        if not status: return False
        if status['error'] == 0 and status['data']['room_status'] == '1':
            return True
        else:
            return False

    @staticmethod
    def get_room_url(room_id: str) -> str:
        return "https://www.DouYu.com/{}".format(room_id)

    def get_rtmp_url(self, room_id: str) -> str:
        """
        打开浏览器获取直播rtmp地址
        :param room_id: 直播间id或别名
        :return: 直播流rtmp地址
        """
        browser = self._init_browser()
        url = self.get_room_url(room_id)
        rtmp_file = os.path.join('/tmp', 'rtmp.dat')
        try:
            old_time = os.path.getmtime(rtmp_file)
        except FileNotFoundError:
            old_time = time.time()
        browser.get(url)
        browser.implicitly_wait(15)
        browser.execute_script('__player.switchPlayer("h5")')
        while not os.path.exists(rtmp_file):
            time.sleep(1)
            print('wait for capture url')
        while old_time >= os.path.getmtime(rtmp_file):
            time.sleep(1)
            print('wait for capture url')
        with open(rtmp_file, 'r', encoding='utf-8') as f:
            rtmp_url = f.read()
        browser.close()

        return rtmp_url

    def start_download_use_ffmpeg(self, url: str, file_name: str, path: str='./') -> None:
        """
        调用ffmpeg进行直播流下载
        :param url: 直播流rtmp地址
        :param file_name: 保存的文件名
        :param path: 保存的地址，默认为当前目录
        :return: None
        """
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(path, file_name)
        subprocess.call(['ffmpeg', '-i', url, '-c', 'copy', path],
                        stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr)


def start() -> None:
    parser = argparse.ArgumentParser(
        prog='DouYu',
        #usage='%(prog)s [options]',
        description='''get DouYu live url and recode it with ffmpeg''')

    parser.add_argument('-p', dest='port', type=str, action='store',
                        help='capture_server的抓包代理接口',
                        default='8080')
    parser.add_argument('room', nargs=1, help='直播间id')
    parser.add_argument('-d', dest='path',nargs='?', action='store', const='./', default='#',
                        help='使用ffmpeg下载到指定地址')

    args = parser.parse_args()
    room_id = args.room[0]
    douyu = DouYu(args.port)
    if not douyu.check_is_living(room_id):
        print('直播并未开始！')
        exit(0)
    url = douyu.get_rtmp_url(room_id)
    print('直播流地址: %s' % url)
    if not args.path == '#':
        path = os.path.dirname(args.path)
        date = time.strftime('%Y-%m-%d-%H:%M:%S')
        file_name = '{date}_{room_id}.flv'.format(date=date, room_id=room_id)
        print('直播流保存到%s' % os.path.realpath(os.path.join(path, file_name)))
        douyu.start_download_use_ffmpeg(url, file_name, path)


if __name__ == '__main__':
    start()
