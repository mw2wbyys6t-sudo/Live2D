#!/usr/bin/env python3
"""
Live2D 官方标准与最佳实践整合 v1.0
基于多维度信息收集：
- Live2D官方文档 (docs.live2d.com)
- B站社区实践 (bilibili.com)
- GitHub开源项目
- 商业约稿标准
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PSDStandard:
    """PSD文件官方标准"""
    # 文件格式要求
    FORMAT: str = "PSD"
    COLOR_MODE: str = "RGB"
    COLOR_CHANNEL: str = "8bit/channel"
    COLOR_PROFILE: str = "sRGB"
    
    # 尺寸标准
    HEAD_MIN_SIZE: int = 1000  # 头部最小1000px
    HEIGHT_MIN: int = 3000     # 整体最小高度
    HEIGHT_MAX: int = 8000     # 最大高度
    DPI: int = 300             # 分辨率
    
    # 边距设置
    ART_MESH_MARGIN: int = 1   # 默认1px边距


@dataclass
class LayerNamingStandard:
    """图层命名标准（多源整合）"""
    
    # 头发层级
    HAIR_BACK = "头发_后"
    HAIR_SIDE_LEFT = "头发_侧发_左"
    HAIR_SIDE_RIGHT = "头发_侧发_右"
    HAIR_FRONT = "头发_刘海"
    HAIR_COW_LICK = "头发_呆毛"
    HAIR_HIGHLIGHT = "头发_高光"
    HAIR_SHADOW = "头发_阴影"
    
    # 面部层级
    FACE_BASE = "脸_基础"
    FACE_BLUSH = "脸_腮红"
    FACE_EYEBROW_LEFT = "眉毛_左"
    FACE_EYEBROW_RIGHT = "眉毛_右"
    FACE_EYE_WHITE_LEFT = "左眼_眼白"
    FACE_EYE_WHITE_RIGHT = "右眼_眼白"
    FACE_EYE_IRIS_LEFT = "左眼_眼珠"
    FACE_EYE_IRIS_RIGHT = "右眼_眼珠"
    FACE_EYE_PUPIL_LEFT = "左眼_瞳孔"
    FACE_EYE_PUPIL_RIGHT = "右眼_瞳孔"
    FACE_EYE_HIGHLIGHT_LEFT = "左眼_高光"
    FACE_EYE_HIGHLIGHT_RIGHT = "右眼_高光"
    FACE_EYE_LASH_UPPER_LEFT = "左眼_上睫毛"
    FACE_EYE_LASH_UPPER_RIGHT = "右眼_上睫毛"
    FACE_EYE_LASH_LOWER_LEFT = "左眼_下睫毛"
    FACE_EYE_LASH_LOWER_RIGHT = "右眼_下睫毛"
    FACE_NOSE = "鼻子"
    FACE_MOUTH_UPPER = "嘴巴_上嘴唇"
    FACE_MOUTH_LOWER = "嘴巴_下嘴唇"
    FACE_MOUTH_INSIDE = "嘴巴_口腔"
    FACE_MOUTH_TONGUE = "嘴巴_舌头"
    FACE_MOUTH_TEETH = "嘴巴_牙齿"
    FACE_EAR_LEFT = "耳朵_左"
    FACE_EAR_RIGHT = "耳朵_右"
    
    # 身体层级
    BODY_NECK = "脖子"
    BODY_CHEST = "胸腔"
    BODY_COLLAR_BONE = "锁骨"
    BODY_WAIST = "腰部"
    BODY_HIPS = "腰臀"
    
    # 手臂层级
    ARM_UPPER_LEFT = "左臂_上臂"
    ARM_LOWER_LEFT = "左臂_下臂"
    ARM_HAND_LEFT = "左手"
    ARM_UPPER_RIGHT = "右臂_上臂"
    ARM_LOWER_RIGHT = "右臂_下臂"
    ARM_HAND_RIGHT = "右手"
    
    # 腿部层级
    LEG_UPPER_LEFT = "左腿_大腿"
    LEG_LOWER_LEFT = "左腿_小腿"
    LEG_FOOT_LEFT = "左脚"
    LEG_UPPER_RIGHT = "右腿_大腿"
    LEG_LOWER_RIGHT = "右腿_小腿"
    LEG_FOOT_RIGHT = "右脚"
    
    # 服装层级
    CLOTHES_OUTER = "衣服_外衣"
    CLOTHES_INNER = "衣服_内衣"
    CLOTHES_ACCESSORY = "饰品"
    
    # 阴影层级
    SHADOW_HEAD_TO_BODY = "阴影_头到身体"
    SHADOW_CLOTHES = "阴影_衣服"


class Live2DQualityStandards:
    """Live2D质量评估标准"""
    
    # 画布尺寸检查
    CANVAS_CHECKS = {
        "head_size": {
            "min": 1000,
            "description": "头部尺寸至少1000px",
            "weight": 0.15
        },
        "height": {
            "min": 3000,
            "max": 8000,
            "description": "整体高度3000-8000px",
            "weight": 0.15
        },
        "dpi": {
            "required": 300,
            "description": "分辨率300dpi",
            "weight": 0.10
        }
    }
    
    # 图层结构检查
    LAYER_CHECKS = {
        "naming": {
            "description": "所有图层必须命名",
            "weight": 0.15
        },
        "no_duplicates": {
            "description": "不能有同名图层",
            "weight": 0.10
        },
        "occlusion_drawn": {
            "description": "遮挡部分必须补全",
            "weight": 0.15
        },
        "gradient_joints": {
            "description": "连接处需要渐变",
            "weight": 0.10
        }
    }
    
    # 颜色与混合模式
    COLOR_CHECKS = {
        "color_mode": {
            "required": "RGB",
            "description": "颜色模式必须为RGB",
            "weight": 0.05
        },
        "blend_mode": {
            "allowed": ["正常", "正片叠底"],
            "description": "仅允许正常和正片叠底",
            "weight": 0.05
        }
    }


class Live2DLayerOrder:
    """Live2D标准图层顺序（从后往前）"""
    
    STANDARD_ORDER = [
        # 背景层
        "背景",
        
        # 后层头发
        "头发_后",
        "头发_阴影_后",
        
        # 身体后层
        "脖子",
        "胸腔",
        "腰臀",
        
        # 腿部
        "左腿_大腿",
        "左腿_小腿",
        "左脚",
        "右腿_大腿",
        "右腿_小腿",
        "右脚",
        
        # 手臂后层
        "左臂_上臂",
        "左臂_下臂",
        "左手",
        "右臂_上臂",
        "右臂_下臂",
        "右手",
        
        # 服装
        "衣服_内衣",
        "衣服_外衣",
        "饰品",
        
        # 面部基础
        "脸_基础",
        "脸_腮红",
        
        # 耳朵
        "耳朵_左",
        "耳朵_右",
        
        # 鼻子
        "鼻子",
        
        # 嘴巴（从里到外）
        "嘴巴_口腔",
        "嘴巴_舌头",
        "嘴巴_牙齿",
        "嘴巴_下嘴唇",
        "嘴巴_上嘴唇",
        
        # 眼睛（从里到外）
        "左眼_眼白",
        "左眼_眼珠",
        "左眼_瞳孔",
        "左眼_高光",
        "右眼_眼白",
        "右眼_眼珠",
        "右眼_瞳孔",
        "右眼_高光",
        
        # 睫毛
        "左眼_下睫毛",
        "右眼_下睫毛",
        "左眼_上睫毛",
        "右眼_上睫毛",
        
        # 眉毛
        "眉毛_左",
        "眉毛_右",
        
        # 前层头发
        "头发_侧发_左",
        "头发_侧发_右",
        "头发_刘海",
        "头发_呆毛",
        "头发_高光",
        
        # 阴影层（正片叠底）
        "阴影_头到身体",
        "阴影_衣服",
    ]


class Live2DGenerationPrompts:
    """Live2D优化生成提示词模板"""
    
    # 基础质量要求
    BASE_QUALITY = """
    高质量，精细细节，清晰线条，
    适合Live2D制作的立绘，
    全身照，正面站立，
    简单背景或透明背景，
    颜色边界清晰，
    遮挡部分完整绘制
    """
    
    # 分层优化提示
    LAYER_OPTIMIZATION = """
    部件分离清晰：
    - 头发分层：前发、侧发、后发
    - 眼睛分层：眼白、眼珠、瞳孔、高光
    - 嘴巴分层：上唇、下唇、口腔内部
    - 身体分层：头、颈、胸、腰、四肢
    - 服装分层：内外衣分开
    """
    
    # 技术规格提示
    TECHNICAL_SPECS = """
    技术规格：
    - 画布尺寸：6000x8000px
    - 分辨率：300dpi
    - 颜色模式：RGB
    - 头部大小：约1200px
    - 线条清晰，颜色边界分明
    """
    
    @classmethod
    def get_full_prompt(cls, character_description: str) -> str:
        """生成完整的Live2D优化提示词"""
        return f"""
        {character_description}
        
        {cls.BASE_QUALITY}
        
        {cls.LAYER_OPTIMIZATION}
        
        {cls.TECHNICAL_SPECS}
        """


class Live2DExportStandards:
    """Live2D导出标准"""
    
    # 必需文件
    REQUIRED_FILES = [
        "model3.json",      # 模型配置
        "*.moc3",           # 模型数据
        "*.png",            # 纹理贴图
    ]
    
    # 可选文件
    OPTIONAL_FILES = [
        "physics.json",     # 物理配置
        "*.motion3.json",   # 动作文件
        "*.pose3.json",     # 姿势文件
        "*.exp3.json",      # 表情文件
    ]
    
    # B站直播姬要求
    BILIBILI_REQUIREMENTS = {
        "format": "ZIP",
        "max_size": "250MB",
        "max_models": 9,
        "naming_rule": "MODEL3.JSON和文件夹名称必须一致",
        "resolution_limit": "过大将自动压缩至2K"
    }


# 实例化标准
PSD_STANDARD = PSDStandard()
LAYER_NAMING = LayerNamingStandard()
QUALITY_STANDARDS = Live2DQualityStandards()
LAYER_ORDER = Live2DLayerOrder()
GENERATION_PROMPTS = Live2DGenerationPrompts()
EXPORT_STANDARDS = Live2DExportStandards()
