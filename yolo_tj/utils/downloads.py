import shutil
import subprocess
from pathlib import Path
from yolo_tj.utils import url2file,clean_url,LOGGER
import requests # 发起 HTTP 请求并处理 HTTP 响应
import torch

GITHUB_ASSETS_NAMES = [f'yolov8{k}{suffix}.pt' for k in 'nsmlx' for suffix in ('', '6', '-cls', '-seg', '-pose')]

GITHUB_ASSETS_STEMS = [Path(k).stem for k in GITHUB_ASSETS_NAMES]

def check_disk_space(url='https://ultralytics.com/assets/coco128.zip',sf=1.5,hard=True):
    r=requests.head(url) #只请求获取目标资源的头部信息，而不会获取资源的实际内容
    assert r.status_code<400,f'URL error for {url}: {r.status_code} {r.reason}'

    gib=1<<30 # 1 千兆字节
    data=int(r.headers.get('Content-Length',0))/gib
    total,used,free=(x/gib for x in shutil.disk_usage('/'))
    if data*sf < free:
        return True
    text = (f'WARNING ⚠️ Insufficient free disk space {free:.1f} GB < {data * sf:.3f} GB required, '
            f'Please free {data * sf - free:.1f} GB additional disk space and try again.')
    if hard:
        raise MemoryError(text)
    LOGGER.warning(text)
    return False






def safe_download(url,
                  file=None,
                  dir=None,
                  unzip=True,
                  delete=False,
                  curl=False,
                  retry=3,
                  min_bytes=1E0,
                  progress=True):
    f = dir / (url2file(url) if dir else Path(file)) # / ?
    if '://' not in str(url) and Path(url).is_file():
        f=Path(url)
    elif not f.is_file():
        assert dir or file , 'dir or file required for download'
        desc=f"Downloading {clean_url(url)} to '{f}'"
        LOGGER.info(f'{desc}...')
        f.parent.mkdir(parents=True,exist_ok=True)
        check_disk_space(url)
        for i in range(retry+1):
            try:
                if curl or i > 0:
                    s='sS' * (not progress) # -s 表示不显示进度，-S表示会显示错误信息，-# 显示进度条，-L 重定向，-o f 保存为f,-C 支持续传 -续传到同名文件
                    r=subprocess.run(['curl','-#',f'-{s}L',url,'-o',f,'--retry','3','-C','-']).returncode
                    assert r==0,f'Curl return value {r}'
                else:
                    method='torch'
                    if method=='torch':
                        torch.hub.download_url_to_file(url,f,progress=progress)
                    else:


