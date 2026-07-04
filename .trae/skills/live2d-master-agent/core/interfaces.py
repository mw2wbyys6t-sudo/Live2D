#!/usr/bin/env python3
"""
Live2D Master Agent - 核心接口定义

定义工作流中各步骤的抽象接口，遵循依赖倒置原则。
所有具体实现必须继承这些抽象类并实现其方法。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class ImageGenerator(ABC):
    """图像生成器接口"""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成图像，返回图像文件路径"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查生成器是否可用"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取生成器名称"""
        pass


class LayerSeparator(ABC):
    """图层分离器接口"""

    @abstractmethod
    def separate(self, image_path: str, output_dir: str) -> List[str]:
        """分离图层，返回图层文件路径列表"""
        pass


class PSDExporter(ABC):
    """PSD导出器接口"""

    @abstractmethod
    def export(self, layers: List[str], output_path: str) -> bool:
        """导出PSD文件，返回是否成功"""
        pass


class QualityAssessor(ABC):
    """质量评估器接口"""

    @abstractmethod
    def assess(self, image_path: str) -> Dict[str, float]:
        """评估图像质量，返回各项质量指标"""
        pass


class WorkflowStep(ABC):
    """工作流步骤接口"""

    @abstractmethod
    def execute(self, context: Dict) -> Dict:
        """执行步骤，接收并返回上下文字典"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取步骤名称"""
        pass

    @abstractmethod
    def can_retry(self) -> bool:
        """步骤是否可重试"""
        pass
