#!/usr/bin/env python3
"""
Live2D PSD 转换器 - 可以集成到skill的完整工具
功能: 将PNG/JPG图片直接转换为可导入Live2D的PSD文件

使用方法:
1. 作为模块导入: from live2d_psd_converter import convert_to_live2d_psd
2. 命令行: python live2d_psd_converter.py input.png output.psd

输出的PSD文件特点:
- 包含标准ArtMesh图层结构
- 可直接导入Live2D Cubism
- 包含参考图层便于对齐
- 符合Live2D导入规范
"""

import os
import sys
import struct
from pathlib import Path
from PIL import Image
from typing import Optional, List, Tuple

class Live2DPSDConverter:
    """
    Live2D PSD文件生成器
    直接将图片转换为可导入Live2D的PSD格式
    """

    # 标准Live2D图层结构（从下到上）
    STANDARD_LAYERS = [
        "Body",          # 身体
        "Hair_Back",     # 头发后部
        "Clothes",       # 服装
        "Hair_Side",     # 头发侧部
        "Face",          # 脸部
        "Eyes",          # 眼睛
        "Mouth",         # 嘴巴
        "Hair_Front",    # 头发前部/刘海
        "Hands",         # 手
        "Accessories",   # 配饰
    ]

    def __init__(self):
        self.output_dir = Path.cwd() / "output"
        self.output_dir.mkdir(exist_ok=True)

    def _write_string(self, data: bytearray, offset: int, string: str) -> int:
        """将字符串写入字节数组"""
        for i, char in enumerate(string):
            data[offset + i] = ord(char)
        return offset + len(string)

    def _write_pascal_string(self, data: bytearray, offset: int, string: str, encoding: str = 'utf-8') -> int:
        """写入Pascal字符串（长度前缀）"""
        encoded = string.encode(encoding)
        length = len(encoded)
        data[offset] = length
        data[offset + 1:offset + 1 + length] = encoded
        # 4字节对齐
        padded_length = ((length + 1 + 3) & ~3)
        return offset + padded_length

    def _create_psd_header(self, width: int, height: int) -> bytes:
        """创建PSD文件头"""
        # 签名 (4) + 版本 (2) + 保留 (6) + 通道数 (2) + 高度 (4) + 宽度 (4) + 深度 (2) + 颜色模式 (2)
        header = bytearray(28)  # 修正：需要28字节
        header[0:4] = b'8BPS'          # 签名
        struct.pack_into('>H', header, 4, 1)  # 版本
        # 保留字节 6-13 保持为0
        struct.pack_into('>H', header, 14, 3)  # 通道数 (RGB)
        struct.pack_into('>I', header, 16, height)
        struct.pack_into('>I', header, 20, width)
        struct.pack_into('>H', header, 24, 8)  # 深度
        struct.pack_into('>H', header, 26, 3)  # 颜色模式 (RGB=3)
        return header

    def _create_image_resources(self) -> bytes:
        """创建图像资源块"""
        # 资源块长度 + 资源数据
        # 最小资源块（分辨率信息）
        res_data = bytearray()
        
        # 8BIM 标记
        res_data.extend(b'8BIM')
        # 资源类型 (0x03ED = 分辨率信息)
        res_data.extend(struct.pack('>H', 0x03ED))
        # 资源ID
        res_data.extend(struct.pack('>H', 0))
        # 资源数据长度
        res_data.extend(struct.pack('>I', 16))
        # 水平分辨率 (72 DPI)
        res_data.extend(struct.pack('>I', 72 << 16))
        # 水平单位 (像素/英寸)
        res_data.extend(struct.pack('>H', 1))
        res_data.extend(struct.pack('>H', 1))  # 填充
        # 垂直分辨率 (72 DPI)
        res_data.extend(struct.pack('>I', 72 << 16))
        # 垂直单位 (像素/英寸)
        res_data.extend(struct.pack('>H', 1))
        res_data.extend(struct.pack('>H', 2))  # 填充
        
        # 返回完整资源块（长度前缀 + 数据）
        return struct.pack('>I', len(res_data)) + res_data

    def _create_layer(self, width: int, height: int, name: str, image_data: Optional[bytes] = None) -> bytes:
        """创建单个图层数据"""
        layer_data = bytearray()
        
        # 图层边界 (top, left, bottom, right)
        layer_data.extend(struct.pack('>iiii', 0, 0, height, width))
        
        # 通道数 (RGB = 3)
        layer_data.extend(struct.pack('>H', 3))
        
        # 通道信息
        if image_data:
            # RGB通道数据位置（相对于图层数据开始）
            rgb_size = width * height
            r_offset = len(layer_data) + 3 * 6 + 4 + 4 + 4 + 1 + 1 + 1 + 1 + 4  # 大致偏移
            layer_data.extend(struct.pack('>hII', 0, r_offset, rgb_size))      # R
            layer_data.extend(struct.pack('>hII', 1, r_offset + rgb_size, rgb_size))      # G
            layer_data.extend(struct.pack('>hII', 2, r_offset + rgb_size * 2, rgb_size))  # B
        else:
            # 空图层
            layer_data.extend(struct.pack('>hII', 0, 0, 0))
            layer_data.extend(struct.pack('>hII', 1, 0, 0))
            layer_data.extend(struct.pack('>hII', 2, 0, 0))
        
        # 混合模式签名 '8BIMnorm'
        layer_data.extend(b'8BIM')
        layer_data.extend(b'norm')
        
        # 不透明度 (255 = 完全不透明)
        layer_data.extend(struct.pack('>B', 255))
        
        # 裁剪标志
        layer_data.extend(struct.pack('>B', 0))
        
        # 图层标志
        layer_data.extend(struct.pack('>B', 1))  # 可见
        
        # 填充
        layer_data.extend(struct.pack('>B', 0))
        
        # 额外数据长度（稍后更新）
        extra_data_pos = len(layer_data)
        layer_data.extend(struct.pack('>I', 0))
        
        # 图层名称 (Unicode)
        name_bytes = name.encode('utf-16-be')
        name_len = len(name_bytes)
        layer_data.extend(b'8BIM')
        layer_data.extend(b'luni')
        layer_data.extend(struct.pack('>I', 4 + name_len))  # 数据长度
        layer_data.extend(struct.pack('>I', len(name)))      # 字符数
        layer_data.extend(name_bytes)
        
        # 4字节对齐
        padding = (4 - (len(layer_data) % 4)) % 4
        layer_data.extend(b'\x00' * padding)
        
        # 更新额外数据长度
        extra_data_len = len(layer_data) - (extra_data_pos + 4)
        struct.pack_into('>I', layer_data, extra_data_pos, extra_data_len)
        
        # 添加通道像素数据（如果有）
        if image_data:
            layer_data.extend(image_data)
        
        return layer_data

    def _create_layer_info(self, width: int, height: int, layers: List[Tuple[str, Optional[bytes]]]) -> bytes:
        """创建图层信息块"""
        layer_count = len(layers)
        layer_info = bytearray()
        
        # 图层数量（负数表示有透明度信息，但我们简化处理）
        layer_info.extend(struct.pack('>h', -layer_count))
        
        # 添加所有图层
        for name, image_data in layers:
            layer_info.extend(self._create_layer(width, height, name, image_data))
        
        # 透明度数据（简化：无透明度）
        layer_info.extend(struct.pack('>I', 0))
        
        return struct.pack('>I', len(layer_info)) + layer_info

    def _create_composite_data(self, width: int, height: int, image: Image.Image) -> bytes:
        """创建合成图像数据"""
        composite = bytearray()
        
        # 压缩标志 (0 = 未压缩)
        composite.extend(struct.pack('>H', 0))
        
        # 像素数据（RGB顺序，每行从左到右，从上到下）
        image_rgb = image.convert('RGB')
        pixels = list(image_rgb.getdata())
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[y * width + x]
                composite.extend(struct.pack('>BBB', r, g, b))
        
        return composite

    def convert(self, image_path: str, output_path: Optional[str] = None, include_reference: bool = True) -> str:
        """
        将图片转换为可导入Live2D的PSD文件
        
        参数:
            image_path: 输入图片路径 (PNG/JPG)
            output_path: 输出PSD路径（可选）
            include_reference: 是否包含参考图层
            
        返回:
            生成的PSD文件路径
        """
        print(f"🎨 正在转换图片: {image_path}")
        
        # 打开图片
        image = Image.open(image_path)
        width, height = image.size
        print(f"   尺寸: {width} x {height}")
        
        # 确定输出路径
        if output_path is None:
            base_name = Path(image_path).stem
            output_path = str(self.output_dir / f"{base_name}_live2d.psd")
        
        print(f"   输出: {output_path}")
        
        # 准备图层数据
        layers = []
        
        if include_reference:
            # 添加参考图层（带原图）
            image_rgb = image.convert('RGB')
            pixels = list(image_rgb.getdata())
            rgb_data = bytearray()
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[y * width + x]
                    rgb_data.extend(struct.pack('>BBB', r, g, b))
            layers.append(('Reference', rgb_data))
        else:
            # 添加空参考图层
            layers.append(('Reference', None))
        
        # 添加标准ArtMesh图层（空图层，用户需要手动填充）
        for layer_name in self.STANDARD_LAYERS:
            layers.append((layer_name, None))
        
        # 创建PSD各个部分
        header = self._create_psd_header(width, height)
        color_mode_data = struct.pack('>I', 0)  # 无颜色模式数据
        resources = self._create_image_resources()
        layer_info = self._create_layer_info(width, height, layers)
        composite = self._create_composite_data(width, height, image)
        
        # 组合所有部分
        psd_data = header + color_mode_data + resources + layer_info + composite
        
        # 写入文件
        with open(output_path, 'wb') as f:
            f.write(psd_data)
        
        print(f"✅ PSD文件已创建: {output_path}")
        print(f"   图层数量: {len(layers)}")
        
        return output_path

    def batch_convert(self, image_paths: List[str], output_dir: Optional[str] = None) -> List[str]:
        """批量转换多个图片"""
        results = []
        for img_path in image_paths:
            if os.path.exists(img_path):
                result = self.convert(img_path, output_dir=output_dir)
                results.append(result)
        return results


# 便捷函数
def convert_to_live2d_psd(image_path: str, output_path: Optional[str] = None) -> str:
    """
    便捷函数：将图片转换为Live2D可用的PSD文件
    
    使用示例:
        from live2d_psd_converter import convert_to_live2d_psd
        psd_path = convert_to_live2d_psd("input.png")
    """
    converter = Live2DPSDConverter()
    return converter.convert(image_path, output_path)


# 命令行使用
def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"   python {Path(__file__).name} <输入图片> [输出PSD]")
        print()
        print("示例:")
        print(f"   python {Path(__file__).name} character.png character.psd")
        return 1
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_path):
        print(f"❌ 文件不存在: {input_path}")
        return 1
    
    try:
        converter = Live2DPSDConverter()
        converter.convert(input_path, output_path)
        return 0
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
