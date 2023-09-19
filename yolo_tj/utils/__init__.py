import logging.config # 使用外部配置文件或代码来配置 Python 的日志系统，以便记录应用程序的信息
import platform
from pathlib import Path
import urllib.parse   #URL 处理、网络请求和与 Web 相关的操作
from tqdm import tqdm as tqdm_original
import os

VERBOSE = str(os.getenv('YOLO_AUTOINSTALL',True)).lower()=='true'
TQDM_BAR_FORMAT='{l_bar}{bar:10}{r_bar}' if VERBOSE else None # 详细输出会打印进度条
LOGGING_NAME = 'ultralytics'
MACOS,LINUX,WINDOWS=(platform.system()==x for x in ['Darwin','Linux','Windows'])

LOGGER = logging.getLogger(LOGGING_NAME)
# 可以在应用程序的不同部分使用相同的 LOGGING_NAME
# 来获取同一个日志记录器，以确保所有的日志消息都记录到同一个地方。

# 将输入的 URL 进行一些规范化和清理操作
def clean_url(url):
    url=Path(url).as_posix().replace(':/','://')
    return urllib.parse.unquote(url).split('?')[0]

def url2file(url):
    return Path(clean_url(url)).name

class TQDM(tqdm_original):
    # *args 用于接受多个位置参数，将它们作为元组传递给函数。
    # **kwargs 用于接受多个关键字参数，将它们作为字典传递给函数。
    def __init__(self,*args,**kwargs):
        kwargs['disable']=not VERBOSE or kwargs.get('disable',False) #
        kwargs.setdefault('bar_format',TQDM_BAR_FORMAT)
        super().__init__(*args,**kwargs)

# 检查网络连接
def is_online()->bool:
    import socket   # 提供了一种在计算机网络中进行套接字编程的方式、

    for host in '1.1.1.1','8.8.8.8','223.5.5.5': # Cloudflare, Google, AliDNS
        try:
            test_connection=socket.create_connection(address=(host,53),timeout=2)
        except (socket.timeout,socket.gaierror,OSError):
            continue
        else:
            test_connection.close()
            return True
    return False

def emojis(string=''):
    """Return platform-dependent emoji-safe version of string."""
    return string.encode().decode('ascii','ignore') if WINDOWS else string