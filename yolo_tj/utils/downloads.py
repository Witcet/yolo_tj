import shutil
import subprocess
from pathlib import Path
from yolo_tj.utils import url2file,clean_url,LOGGER,TQDM,is_online,emojis
import requests # 发起 HTTP 请求并处理 HTTP 响应
import torch
from urllib import request

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



def unzip_file(file,path=None,exclude=('.DS_Store','__MACOSX'),progres=True):
    from zipfile import BadZipfile,ZipFile,is_zipfile   # 提供了用于创建、读取和处理 ZIP 文件的工具

    if not (Path(file).exists() and is_zipfile(file)):
        raise BadZipfile(f"File '{file}' does not exist or is a bad zip file.")
    if path is None:
        path=Path(file).parent

    with ZipFile(file) as zipObj:
        # todo




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
                        with request.urlopen(url) as response,TQDM(total=int(response.getheader('Content-Length',0)), # 指定定总进度的大小
                                                                   desc=desc, # 描述性文本
                                                                   disable=not progress, # 是否显示过程
                                                                   unit='B',    # 单位（字节）
                                                                   unit_scale=True, # 自动调整单位，如KB，MB
                                                                   unit_divisor=1024) as pbar: # 单位划分的基数 默认1000
                            with open(f,'wb') as f_opened:
                                for data in response:
                                    f_opened.write(data)
                                    pbar.update(len(data)) # 更新进度条

                if f.exists():
                    if f.stat().st_size>min_bytes: # 下载的文件足够大，下载成功
                        break
                    f.unlink() # 否则删除该文件
            except Exception as e:
                if i==0 and not is_online():
                    raise ConnectionError(emojis(f'❌ Download failure for {url}. Environment is not online.')) from e
                elif i>=retry:
                    raise ConnectionError(emojis(f'❌  Download failure for {url}. Retry limit reached.')) from e
                LOGGER.warning(f'⚠️ Download failure, retrying {i + 1}/{retry} {url}...')

    if unzip and f.exists() and f.suffix in ('','.zip','.tar','gz'):
        from zipfile import is_zipfile

        unzip_dir = dir or f.parent
        if  is_zipfile(f):
            unzip_dir=unzip_file


