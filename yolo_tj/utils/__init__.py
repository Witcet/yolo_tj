import logging.config # 使用外部配置文件或代码来配置 Python 的日志系统，以便记录应用程序的信息
from pathlib import Path
import urllib.parse   #URL 处理、网络请求和与 Web 相关的操作

LOGGING_NAME = 'ultralytics'

LOGGER = logging.getLogger(LOGGING_NAME)
# 可以在应用程序的不同部分使用相同的 LOGGING_NAME
# 来获取同一个日志记录器，以确保所有的日志消息都记录到同一个地方。

# 将输入的 URL 进行一些规范化和清理操作
def clean_url(url):
    url=Path(url).as_posix().replace(':/','://')
    return urllib.parse.unquote(url).split('?')[0]

def url2file(url):
    return Path(clean_url(url)).name