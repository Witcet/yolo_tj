import re
from pathlib import Path
from yolo_tj.utils import LOGGER, url2file, clean_url, downloads


# 改以前的文件名
def check_yolov5u_filename(file: str, verbose: bool = True):
    if 'yolov3' in file or 'yolov5' in file:
        if 'u.yaml' in file:
            file = file.replace('u.yaml', '.yaml')  # yolov5nu.yaml -> yolov5n.yaml
        elif '.pt' in file and 'u' not in file:
            original_file = file
            file = re.sub(r'(.*yolov5([nsmlx)]))\.pt', '\\1u.pt', file)
            file = re.sub(r'(.*yolov5([nsmlx])6)\.pt', '\\1u.pt', file)  # i.e. yolov5n6.pt -> yolov5n6u.pt
            file = re.sub(r'(.*yolov3(|-tiny|-spp))\.pt', '\\1u.pt', file)  # i.e. yolov3-spp.pt -> yolov3-sppu.pt
            if file != original_file and verbose:
                LOGGER.info(LOGGER.info(
                    f"PRO TIP 💡 Replace 'model={original_file}' with new 'model={file}'.\nYOLOv5 'u' models are "
                    f'trained with https://github.com/ultralytics/ultralytics and feature improved performance vs '
                    f'standard YOLOv5 models trained with https://github.com/ultralytics/yolov5.\n'))
    return file


def check_suffix(file='yolov8n.pt', suffix='.pt', msg=''):
    if file and suffix:
        if isinstance(suffix, str):
            suffix = (suffix,)  # 将字符串类型转成元组
        for f in file if isinstance(file, (list, tuple)) else [file]:  # 确保file是列表
            s = Path(f).suffix.lower().strip()
            if len(s):
                assert s in suffix, f'{msg}{f} acceptable suffix is {suffix}, not {s}'


def check_file(file, suffix='', download=True, hard=True):
    check_suffix(file, suffix)
    file = str(file).strip()
    file = check_yolov5u_filename(file)
    if not file or ('://' not in file and Path(file).exists()):
        return file
    elif download and file.lower().startswith(('https://', 'http://', 'rtsp://', 'rtmp://')):
        url = file
        file = url2file(file)
        if Path(file).exists():
            LOGGER.info(f'Found {clean_url(url)} locally at {file}')
        else:
            download.safe_download(url=url, file=file, unzip=False)


def check_yaml(file, suffix=('.yaml', '.yml'), hard=True):
    return
