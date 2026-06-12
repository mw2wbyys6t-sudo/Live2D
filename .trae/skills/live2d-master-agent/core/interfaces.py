#!/usr/bin/env python3
"""
Live2D Master Agent - 核心接口定义模块
定义所有核心组件的抽象接口，实现依赖倒置原则
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Tuple
from pathlib import Path


class ImageGenerator(ABC):
    """图像生成器接口"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成图片并返回路径"""
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
    """图像分层器接口"""
    
    @abstractmethod
    def separate(self, image_path: str, output_dir: str) -> List[str]:
        """对图片进行分层，返回图层路径列表"""
        pass
    
    @abstractmethod
    def get_layer_names(self) -> List[str]:
        """获取标准图层名称列表"""
        pass


class PSDExporter(ABC):
    """PSD导出器接口"""
    
    @abstractmethod
    def export(self, layers: List[str], output_path: str) -> bool:
        """导出PSD文件"""
        pass
    
    @abstractmethod
    def validate(self, psd_path: str) -> bool:
        """验证PSD文件是否符合Live2D标准"""
        pass


class QualityAssessor(ABC):
    """质量评估器接口"""
    
    @abstractmethod
    def assess(self, image_path: str) -> Dict[str, float]:
        """评估图片质量，返回各维度评分"""
        pass
    
    @abstractmethod
    def is_suitable_for_live2d(self, scores: Dict[str, float]) -> bool:
        """判断是否适合Live2D使用"""
        pass


class WorkflowStep(ABC):
    """工作流步骤接口"""
    
    @abstractmethod
    def execute(self, context: Dict) -> Dict:
        """执行步骤，接收上下文并返回更新后的上下文"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取步骤名称"""
        pass
    
    @abstractmethod
    def can_retry(self) -> bool:
        """是否支持重试"""
        pass
