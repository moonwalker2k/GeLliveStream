from setuptools import setup
from DouYu import __version__ as version

setup(
    name='DouYu',
    version= version,
    description='douyu直播爬虫，爬取直播流, 调用ffmpeg进行直播下载',
    author='moonwalker',
    author_email='moonwalker2k@outlook.com',
    packages=['DouYu'],
    install_requires=[    # 依赖列表
        'requests>=2.18.4',
        'selenium>=3.11.0',
        'mitmproxy>=3.0.3'
    ],
    entry_points={
        'console_scripts': [
            'douyu = DouYu.douyu:start',
            'douyu_capture_server = DouYu.douyu_capture_server:start'
        ]
    }
)