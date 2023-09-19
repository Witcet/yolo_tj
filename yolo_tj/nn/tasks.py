from pathlib import Path
from yolo_tj.utils import LOGGER

# 从yaml文件加载模型
def yaml_model_load(path):
    import re # 导入正则表达式模块，用于搜索匹配
    path=Path(path)
    #把以前的YOLO P6 models的后缀修改成-p6"
    if path.stem in (f'yolov{d}{x}6' for x in 'nsmlx' for d in (5,8)):
        new_stem=re.sub(r'(\d+)([nsmlx])6(.+)?$',r'\1\2-p6\3',path.stem)
        LOGGER.warning(f'WARNING ⚠️ Ultralytics YOLO P6 models now use -p6 suffix. Renaming {path.stem} to {new_stem}.')
        path=path.with_name(new_stem+path.suffix)
    # 删除nsmlx
    unified_path=re.sub(r'(\d+)([nslmx)])(.+)?$',r'\1\3',str(path))
    yaml_file= check_yaml(unified_path,hard=False)

