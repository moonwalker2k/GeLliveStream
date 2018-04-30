网络直播流获取
==============
## 安装
* 需要安装pip和python3
* 使用前确保已经安装好系统Chrome对应版本的[chromedriver](https://sites.google.com/a/chromium.org/chromedriver/), [国内镜像](http://npm.taobao.org/mirrors/chromedriver/)
* 管理员运行 ```python3 setup.py insatall```

## 使用
单一个终端运行
```$ douyu_capture_server```
另一个终端运行
```$ douyu 24422```
即可获得```https://www.douyu.com/24422```的直播流地址
加参数```'-d'```可以调用ffmpeg下载直播流到当前目录，具体查看```'-h```
## 依赖
* ```Chrome/Chromium```浏览器
* 所需的库
    * ```requests```
    * ```selenium```
    * ```mitmproxy```
* （可选）ffmpeg
* 使用前确保已经安装好系统Chrome对应版本的[chromedriver](https://sites.google.com/a/chromium.org/chromedriver/), [国内镜像](http://npm.taobao.org/mirrors/chromedriver/)
* 暂时只支持斗鱼直播
* 务必先启动```douyu_capture_server```, 再启动```douyu```进行使用