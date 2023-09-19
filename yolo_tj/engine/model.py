import torch.nn as nn       #包含了构建神经网络和深度学习模型所需的核心组件\
from typing import Union    #指定一个变量可以接受多种不同类型的值
from pathlib import Path    #处理文件系统路径和文件操作
from yolo_tj.utils import callbacks
from yolo_tj.utils.downloads import GITHUB_ASSETS_STEMS

class Model(nn.Module):
    # Union type; Union[X, Y] means either X or Y.
    def __init__(self,model: Union[str,Path] = "yolov8n.pt", task=None)-> None:
        super.__init__()
        # 全部变量和回调函数初始化为空
        self.callbacks=callbacks.get_default_callbacks()
        self.predictor = None  # reuse predictor
        self.model = None  # model object
        self.trainer = None  # trainer object
        self.ckpt = None  # if loaded from *.pt
        self.cfg = None  # if loaded from *.yaml
        self.ckpt_path = None
        self.overrides = {}  # overrides for trainer object
        self.metrics = None  # validation/training metrics
        self.task = task  # task type
        # 防止输入头尾含有空格
        model=str(model).strip()

        suffix=Path(model).suffix
        #如果输入没有后缀，只要模型名称正确，就可以后续从github库里下载该模型
        if not suffix and Path(model).stem in GITHUB_ASSETS_STEMS:
            model,suffix = Path(model).with_suffix('.pt'),'.pt'
        # 对于输入不是pt模型，而是yaml文件
        if suffix in ('.yaml','yml'):
            self._new(model,task)
        else:
            self._load(model,task)

    def __call__(self):
        pass

    def _new(self,cfg:str,task=None,model=None,verbose=True):
        cfg_dict=yaml_model_load(cfg)







