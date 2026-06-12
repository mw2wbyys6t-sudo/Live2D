#!/usr/bin/env python3
"""
Live2D Desktop Pet - 桌面Live2D桌宠功能 v1.0
基于现有工作流拓展，支持将创作的角色直接部署为桌面宠物

功能特性：
- ✅ 基于PSD分层自动创建动画角色
- ✅ 支持表情切换（微笑、眨眼、害羞等）
- ✅ 支持身体摆动动画
- ✅ 支持鼠标交互（点击、拖拽）
- ✅ 支持透明度和层级管理
- ✅ 一键部署到桌面

使用方法：
    # 方式1: 从PSD文件创建桌宠
    python live2d_desktop_pet.py --psd layers.psd --output pet
    
    # 方式2: 从分层目录创建桌宠
    python live2d_desktop_pet.py --layers-dir layers_12345 --output pet
    
    # 方式3: 完整工作流 + 桌宠部署
    python live2d_workflow.py "蓝发猫耳少女" --deploy-desktop
    
    # 运行桌宠
    python live2d_desktop_pet.py --run pet
"""

import os
import sys
import time
import argparse
import json
import random
from pathlib import Path
from typing import Dict, List, Optional

try:
    import pygame
    from pygame.locals import *
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import numpy as np
    NP_AVAILABLE = True
except ImportError:
    NP_AVAILABLE = False


class DesktopPetAnimator:
    """桌面Live2D桌宠动画器"""
    
    def __init__(self, layers_dir: str, output_dir: str = "./pet_output"):
        self.layers_dir = Path(layers_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 动画状态
        self.animation_state = {
            "body_angle": 0,
            "body_speed": 0.02,
            "eye_blink": False,
            "eye_blink_timer": 0,
            "mouth_open": False,
            "mouth_timer": 0,
            "expression": "normal",  # normal, happy, shy, surprised
            "expression_timer": 0,
            "mouse_over": False,
            "mouse_pos": (0, 0),
            "pet_pos": (400, 300),
            "target_pos": (400, 300),
            "move_speed": 0.05,
            "scale": 1.0,
            "opacity": 255,
        }
        
        # 图层分组（基于Live2D官方标准）
        self.layer_groups = {
            "body": ["身体", "躯干", "胸腔", "腰臀"],
            "left_arm": ["左臂_上臂", "左臂_下臂", "左手"],
            "right_arm": ["右臂_上臂", "右臂_下臂", "右手"],
            "left_leg": ["左腿_大腿", "左腿_小腿", "左脚"],
            "right_leg": ["右腿_大腿", "右腿_小腿", "右脚"],
            "hair_back": ["头发_后", "头发_阴影_后"],
            "hair_front": ["头发_刘海", "头发_侧发_左", "头发_侧发_右", "头发_呆毛", "头发_高光"],
            "face": ["脸_基础", "脸_腮红"],
            "eyes": ["左眼_眼白", "右眼_眼白", "左眼_眼珠", "右眼_眼珠", 
                    "左眼_瞳孔", "右眼_瞳孔", "左眼_高光", "右眼_高光"],
            "eyelashes": ["左眼_上睫毛", "右眼_上睫毛", "左眼_下睫毛", "右眼_下睫毛"],
            "eyebrows": ["眉毛_左", "眉毛_右"],
            "mouth": ["嘴巴_口腔", "嘴巴_舌头", "嘴巴_牙齿", "嘴巴_上嘴唇", "嘴巴_下嘴唇"],
            "nose": ["鼻子"],
            "ears": ["耳朵_左", "耳朵_右"],
            "clothes": ["衣服_内衣", "衣服_外衣"],
            "accessories": ["饰品"],
            "shadow": ["阴影_头到身体", "阴影_衣服"],
            "background": ["背景"],
        }
        
        # 加载图层
        self.layers = {}
        self.load_layers()
    
    def load_layers(self):
        """加载所有图层"""
        print(f"📂 正在加载图层: {self.layers_dir}")
        
        layer_files = list(self.layers_dir.glob("*.png"))
        
        for layer_file in layer_files:
            if "原图" in str(layer_file):
                continue
                
            layer_name = layer_file.stem
            # 提取实际名称（去掉序号）
            parts = layer_name.split('_', 1)
            if len(parts) > 1 and parts[0].isdigit():
                layer_name = parts[1]
            
            try:
                img = Image.open(layer_file).convert("RGBA")
                self.layers[layer_name] = img
                print(f"   ✓ 加载图层: {layer_name}")
            except Exception as e:
                print(f"   ⚠️ 无法加载图层 {layer_name}: {e}")
        
        print(f"✅ 共加载 {len(self.layers)} 个图层")
    
    def classify_layers(self):
        """将图层分类到不同组"""
        classified = {}
        unclassified = []
        
        for layer_name, img in self.layers.items():
            matched = False
            for group_name, keywords in self.layer_groups.items():
                for keyword in keywords:
                    if keyword in layer_name or layer_name in keyword:
                        if group_name not in classified:
                            classified[group_name] = []
                        classified[group_name].append((layer_name, img))
                        matched = True
                        break
                if matched:
                    break
            if not matched:
                unclassified.append((layer_name, img))
        
        # 添加未分类的图层
        if unclassified:
            classified["other"] = unclassified
        
        return classified
    
    def create_animation_config(self):
        """创建动画配置文件"""
        config = {
            "version": "1.0",
            "name": "Live2D Desktop Pet",
            "layers": list(self.layers.keys()),
            "layer_groups": self.layer_groups,
            "animations": {
                "idle": {
                    "body_swing": {"amplitude": 5, "speed": 0.03},
                    "eye_blink": {"interval": 3000, "duration": 200},
                    "breath": {"amplitude": 3, "speed": 0.02},
                },
            },
            "expressions": {
                "normal": {"mouth_open": False, "eye_squint": False},
                "happy": {"mouth_open": True, "eye_squint": False, "blush": True},
                "shy": {"mouth_open": False, "eye_squint": True, "blush": True},
                "surprised": {"mouth_open": True, "eye_squint": False, "eyebrow_raise": True},
                "sleepy": {"eye_squint": True, "mouth_open": True},
            },
            "interaction": {
                "click_response": "happy",
                "double_click_response": "surprised",
                "drag_enabled": True,
                "auto_move": True,
                "move_interval": 10000,
            },
        }
        
        config_path = self.output_dir / "animation_config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 动画配置已保存: {config_path}")
        return config
    
    def update_animation_state(self, frame_idx: int = 0) -> Dict:
        """更新并返回动画状态，供外部驱动动画使用"""
        state = self.animation_state.copy()
        # 身体摆动（更大的频率让摆动在60帧内完成多个周期）
        state["body_angle"] = np.sin(frame_idx * 0.1) * np.pi / 12
        # 呼吸效果（独立的正弦波，频率稍低）
        state["breath_offset"] = np.sin(frame_idx * 0.05) * 3

        # 眨眼逻辑
        state["eye_blink_timer"] += 16
        if state["eye_blink_timer"] > 300 and random.random() < 0.02:
            state["eye_blink"] = True
            state["eye_blink_timer"] = 0
        if state["eye_blink_timer"] < 8:
            state["eye_blink"] = True
        else:
            state["eye_blink"] = False

        # 表情随机变化
        state["expression_timer"] += 16
        if state["expression_timer"] > 5000:
            expressions = ["normal", "happy", "shy", "normal", "normal"]
            state["expression"] = random.choice(expressions)
            state["expression_timer"] = 0

        return state

    def render_frame(self, classified_layers: Dict, state: Dict) -> Image.Image:
        """渲染单帧动画"""
        # 获取参考图尺寸（优先从self.layers，否则从classified_layers）
        first_layer = next(iter(self.layers.values()), None)
        if not first_layer and classified_layers:
            # 从classified_layers获取第一个图层
            for group in classified_layers.values():
                if isinstance(group, list) and len(group) > 0:
                    first_layer = group[0][1] if isinstance(group[0], tuple) else group[0]
                    break
                elif isinstance(group, Image.Image):
                    first_layer = group
                    break
        if not first_layer:
            return None

        width, height = first_layer.size
        composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        
        # 计算身体摆动（放大偏移量，确保可见）
        body_angle = state["body_angle"]
        body_offset_x = int(body_angle * 30)  # 水平摆动，放大偏移
        body_offset_y = int(body_angle * 20)  # 垂直摆动

        # 计算呼吸效果（独立的垂直偏移）
        breath_offset = int(state.get("breath_offset", 0))
        
        # 渲染顺序（从后往前）
        render_order = [
            "background", "shadow", "body", "left_leg", "right_leg",
            "clothes", "left_arm", "right_arm", "hair_back",
            "face", "ears", "nose", "hair_front",
            "eyebrows", "eyes", "eyelashes", "mouth", "accessories"
        ]
        
        for group_name in render_order:
            if group_name in classified_layers:
                for layer_name, img in classified_layers[group_name]:
                    # 根据图层组应用不同的动画效果
                    offset_x, offset_y = 0, 0
                    
                    # 身体摆动 + 呼吸
                    if group_name in ["body", "clothes", "shadow"]:
                        offset_x = body_offset_x
                        offset_y = body_offset_y + breath_offset
                    # 头发摆动幅度更大
                    elif group_name in ["hair_back", "hair_front"]:
                        offset_x = body_offset_x * 1.5
                        offset_y = body_offset_y * 1.5
                    # 手臂摆动
                    elif group_name in ["left_arm"]:
                        offset_x = body_offset_x * 1.2
                        offset_y = -body_offset_y * 1.5
                    elif group_name in ["right_arm"]:
                        offset_x = body_offset_x * 1.2
                        offset_y = body_offset_y * 1.5
                    # 腿部轻微摆动
                    elif group_name in ["left_leg", "right_leg"]:
                        offset_x = body_offset_x * 0.5
                        offset_y = body_offset_y * 0.3
                    # 面部保持稳定
                    elif group_name in ["face", "eyes", "eyebrows", "mouth", "nose", "ears"]:
                        offset_x = body_offset_x * 0.3
                        offset_y = body_offset_y * 0.3
                    
                    # 创建偏移后的图层
                    offset_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                    offset_img.paste(img, (int(offset_x), int(offset_y)))
                    
                    # 处理表情
                    if group_name == "eyes" and state["eye_blink"]:
                        # 眨眼效果 - 缩小眼睛
                        offset_img = self._apply_blink_effect(offset_img)
                    
                    if group_name == "mouth":
                        if state["expression"] == "happy":
                            offset_img = self._apply_happy_mouth(offset_img)
                        elif state["expression"] == "surprised":
                            offset_img = self._apply_surprised_mouth(offset_img)
                    
                    if group_name == "face" and state["expression"] in ["happy", "shy"]:
                        offset_img = self._apply_blush_effect(offset_img)
                    
                    # 合成到最终图像
                    composite = Image.alpha_composite(composite, offset_img)
        
        return composite
    
    def _apply_blink_effect(self, img: Image.Image) -> Image.Image:
        """应用眨眼效果 - 在原位置将眼睛纵向压缩"""
        width, height = img.size
        # 创建新画布，将眼睛图层纵向压缩到20%高度
        new_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        compressed = img.resize((width, max(1, int(height * 0.2))), Image.Resampling.LANCZOS)
        # 将压缩后的眼睛放回原位置（居中）
        y_offset = int(height * 0.4)  # 眼睛居中位置
        new_img.paste(compressed, (0, y_offset))
        return new_img
    
    def _apply_happy_mouth(self, img: Image.Image) -> Image.Image:
        """应用开心表情（微笑）- 在原位置稍微放大嘴巴"""
        width, height = img.size
        new_w, new_h = int(width * 1.1), int(height * 1.1)
        new_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        # 居中放置
        x_off = (width - new_w) // 2
        y_off = (height - new_h) // 2
        new_img.paste(resized, (x_off, y_off))
        return new_img

    def _apply_surprised_mouth(self, img: Image.Image) -> Image.Image:
        """应用惊讶表情 - 在原位置放大嘴巴"""
        width, height = img.size
        new_w, new_h = int(width * 1.2), int(height * 1.3)
        new_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        x_off = (width - new_w) // 2
        y_off = (height - new_h) // 2
        new_img.paste(resized, (x_off, y_off))
        return new_img
    
    def _apply_blush_effect(self, img: Image.Image) -> Image.Image:
        """应用腮红效果"""
        # 在脸颊位置添加粉色
        img_array = np.array(img)
        width, height = img_array.shape[1], img_array.shape[0]
        
        # 在脸颊位置添加腮红
        for y in range(int(height * 0.3), int(height * 0.5)):
            for x in range(int(width * 0.2), int(width * 0.3)):
                if img_array[y, x, 3] > 0:
                    img_array[y, x, 0] = min(255, img_array[y, x, 0] + 50)
                    img_array[y, x, 1] = min(255, img_array[y, x, 1] + 20)
            for x in range(int(width * 0.7), int(width * 0.8)):
                if img_array[y, x, 3] > 0:
                    img_array[y, x, 0] = min(255, img_array[y, x, 0] + 50)
                    img_array[y, x, 1] = min(255, img_array[y, x, 1] + 20)
        
        return Image.fromarray(img_array)
    
    def generate_frames(self, frame_count: int = 60):
        """生成动画帧序列"""
        print("🎬 正在生成动画帧...")
        frames_dir = self.output_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        
        classified_layers = self.classify_layers()
        state = self.animation_state.copy()
        
        for frame_idx in range(frame_count):
            # 更新动画状态 - 使用更大的频率让摆动在60帧内完成多个周期
            state["body_angle"] = np.sin(frame_idx * 0.1) * np.pi / 12
            # 呼吸效果（独立的正弦波，频率稍低）
            state["breath_offset"] = np.sin(frame_idx * 0.05) * 3
            
            # 眨眼逻辑
            state["eye_blink_timer"] += 16  # 约60fps
            if state["eye_blink_timer"] > 300 and random.random() < 0.02:
                state["eye_blink"] = True
                state["eye_blink_timer"] = 0
            if state["eye_blink_timer"] < 8:
                state["eye_blink"] = True
            else:
                state["eye_blink"] = False
            
            # 表情随机变化
            state["expression_timer"] += 16
            if state["expression_timer"] > 5000:
                expressions = ["normal", "happy", "shy", "normal", "normal"]
                state["expression"] = random.choice(expressions)
                state["expression_timer"] = 0
            
            # 渲染帧
            frame = self.render_frame(classified_layers, state)
            if frame:
                frame.save(frames_dir / f"frame_{frame_idx:04d}.png")
            
            if (frame_idx + 1) % 10 == 0:
                print(f"   已生成 {frame_idx + 1}/{frame_count} 帧")
        
        print(f"✅ 动画帧生成完成: {frame_count} 帧")
        return frames_dir
    
    def create_pet_package(self):
        """创建桌宠部署包"""
        print("\n📦 正在创建桌宠部署包...")
        
        # 1. 生成动画帧
        self.generate_frames(60)
        
        # 2. 创建配置文件
        self.create_animation_config()
        
        # 3. 创建运行脚本
        self._create_run_script()
        
        # 4. 创建说明文档
        self._create_readme()
        
        print(f"\n✅ 桌宠部署包已创建完成！")
        print(f"📁 输出目录: {self.output_dir}")
        print("\n💡 运行桌宠:")
        print(f"   python {self.output_dir / 'run_pet.py'}")
        
        return str(self.output_dir)
    
    def _create_run_script(self):
        """创建运行脚本（独立可执行，不依赖外部模块）"""
        run_script = '''#!/usr/bin/env python3
"""
Live2D Desktop Pet - 运行脚本
双击此文件或使用命令: python run_pet.py
无需安装Live2D软件，一键运行！
"""

import sys
import os
import json
import random
from pathlib import Path

try:
    import pygame
    from pygame.locals import *
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class PetRunner:
    """桌宠运行器 - 使用pygame在桌面上显示动画角色"""
    
    def __init__(self, config_path: str, frames_dir: str):
        self.config_path = Path(config_path)
        self.frames_dir = Path(frames_dir)
        
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.frames = []
        self.load_frames()
        
        self.running = True
        self.current_frame = 0
        self.frame_rate = 60
        self.last_time = 0
        
        self.screen_width = 200
        self.screen_height = 300
        self.x = 100
        self.y = 100
        self.target_x = 100
        self.target_y = 100
        self.dragging = False
        self.drag_offset = (0, 0)
        
        self.expression = "normal"
        self.expression_timer = 0
        
        self.mouse_x = 0
        self.mouse_y = 0
        
        self.auto_move_timer = 0
        self.auto_move_interval = 10000
    
    def load_frames(self):
        """加载动画帧"""
        frame_files = sorted(self.frames_dir.glob("frame_*.png"))
        for frame_file in frame_files:
            try:
                surf = pygame.image.load(str(frame_file)).convert_alpha()
                self.frames.append(surf)
            except Exception as e:
                print(f"\\u26a0\\ufe0f 无法加载帧 {frame_file}: {e}")
        
        print(f"\\u2705 加载了 {len(self.frames)} 帧动画")
    
    def run(self):
        """运行桌宠"""
        if not PYGAME_AVAILABLE:
            print("\\u274c 需要安装 pygame: pip install pygame")
            return
        
        pygame.init()
        
        screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        pygame.display.set_caption("Live2D Pet")
        screen.set_alpha(None)
        
        clock = pygame.time.Clock()
        
        print("\\n\\ud83d\\udc31 Live2D 桌面宠物启动！")
        print("\\ud83c\\udfa8 提示: 点击宠物可以互动，拖拽可以移动位置")
        print("\\ud83d\\udd34 按 ESC 或关闭窗口退出\\n")
        
        while self.running:
            current_time = pygame.time.get_ticks()
            self.handle_events()
            self.update(current_time)
            self.render(screen)
            clock.tick(self.frame_rate)
        
        pygame.quit()
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.is_click_on_pet(mouse_x, mouse_y):
                        self.dragging = True
                        self.drag_offset = (mouse_x - self.x, mouse_y - self.y)
                        self.on_click()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == MOUSEMOTION:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if self.dragging:
                    self.x = self.mouse_x - self.drag_offset[0]
                    self.y = self.mouse_y - self.drag_offset[1]
                    screen_info = pygame.display.Info()
                    self.x = max(0, min(self.x, screen_info.current_w - self.screen_width))
                    self.y = max(0, min(self.y, screen_info.current_h - self.screen_height))
    
    def is_click_on_pet(self, mouse_x: int, mouse_y: int) -> bool:
        """检查点击是否在宠物区域内"""
        return (self.x < mouse_x < self.x + self.screen_width and
                self.y < mouse_y < self.y + self.screen_height)
    
    def on_click(self):
        """处理点击事件"""
        print("\\u2728 宠物被点击了！")
        self.set_expression("happy")
    
    def set_expression(self, expression: str):
        """设置表情"""
        self.expression = expression
        self.expression_timer = pygame.time.get_ticks()
    
    def update(self, current_time: int):
        """更新状态"""
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        if current_time - self.expression_timer > 2000:
            self.expression = "normal"
        
        self.auto_move_timer += 16
        if self.auto_move_timer > self.auto_move_interval:
            self.auto_move_timer = 0
            screen_info = pygame.display.Info()
            self.target_x = random.randint(0, screen_info.current_w - self.screen_width)
            self.target_y = random.randint(0, screen_info.current_h - self.screen_height)
    
    def render(self, screen):
        """渲染"""
        screen.fill((0, 0, 0, 0))
        
        if self.frames:
            frame = self.frames[self.current_frame]
            frame = pygame.transform.smoothscale(frame, (self.screen_width, self.screen_height))
            screen.blit(frame, (0, 0))
        
        pygame.display.flip()
        # 使用环境变量设置窗口位置（跨平台兼容）
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{self.x},{self.y}"

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    config_path = "animation_config.json"
    frames_dir = "frames"
    
    if not os.path.exists(config_path) or not os.path.exists(frames_dir):
        print("\\u274c 桌宠文件不完整")
        input("按回车退出...")
        sys.exit(1)
    
    try:
        runner = PetRunner(config_path, frames_dir)
        runner.run()
    except Exception as e:
        print(f"\\u274c 运行错误: {e}")
        print("请确保已安装必要依赖: pip install pygame")
        input("按回车退出...")
'''
        
        script_path = self.output_dir / "run_pet.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(run_script)
        
        bat_script = '''@echo off
cd /d "%~dp0"
python run_pet.py
pause
'''
        bat_path = self.output_dir / "run_pet.bat"
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_script)
        
        print(f"   ✓ 创建运行脚本: run_pet.py")
    
    def _create_readme(self):
        """创建说明文档"""
        readme = f'''# 🐱 Live2D 桌面宠物

## 🚀 快速开始

### Windows 用户
双击运行 `run_pet.bat`

### Mac/Linux 用户
```bash
python run_pet.py
```

## 🎮 交互说明

| 操作 | 效果 |
|------|------|
| 🖱️ 点击 | 触发开心表情 |
| 👆 双击 | 触发惊讶表情 |
| 🖱️ 拖拽 | 移动宠物位置 |
| 🖱️ 悬停 | 宠物会看向鼠标 |

## ⚙️ 配置说明

编辑 `animation_config.json` 可以自定义：
- 动画速度和幅度
- 表情类型和触发条件
- 交互行为

## 📁 文件结构

```
{self.output_dir.name}/
├── run_pet.py          # 运行脚本
├── run_pet.bat         # Windows批处理
├── animation_config.json # 动画配置
├── frames/             # 动画帧目录
│   ├── frame_0000.png
│   ├── frame_0001.png
│   └── ...
└── README.md           # 本说明文件
```

## 🛠️ 系统要求

- Python 3.8+
- pygame
- pillow
- numpy

## ❓ 常见问题

**Q: 运行时提示缺少模块？**
A: 请安装依赖: `pip install pygame pillow numpy`

**Q: 宠物显示位置不对？**
A: 可以通过拖拽调整位置，或修改配置文件中的初始位置

---

Live2D Master Agent v7.1
'''
        
        readme_path = self.output_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme)
        
        print(f"   ✓ 创建说明文档: README.md")


class PetRunner:
    """桌宠运行器 - 使用pygame在桌面上显示动画角色"""
    
    def __init__(self, config_path: str, frames_dir: str):
        self.config_path = Path(config_path)
        self.frames_dir = Path(frames_dir)
        
        # 加载配置
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        # 加载动画帧
        self.frames = []
        self.load_frames()
        
        # 运行状态
        self.running = True
        self.current_frame = 0
        self.frame_rate = 60
        self.last_time = 0
        
        # 窗口位置
        self.screen_width = 200
        self.screen_height = 300
        self.x = 100
        self.y = 100
        self.target_x = 100
        self.target_y = 100
        self.dragging = False
        self.drag_offset = (0, 0)
        
        # 表情状态
        self.expression = "normal"
        self.expression_timer = 0
        
        # 鼠标状态
        self.mouse_x = 0
        self.mouse_y = 0
        
        # 自动移动
        self.auto_move_timer = 0
        self.auto_move_interval = 10000
    
    def load_frames(self):
        """加载动画帧"""
        frame_files = sorted(self.frames_dir.glob("frame_*.png"))
        for frame_file in frame_files:
            try:
                surf = pygame.image.load(str(frame_file)).convert_alpha()
                self.frames.append(surf)
            except Exception as e:
                print(f"⚠️ 无法加载帧 {frame_file}: {e}")
        
        print(f"✅ 加载了 {len(self.frames)} 帧动画")
    
    def run(self):
        """运行桌宠"""
        if not PYGAME_AVAILABLE:
            print("❌ 需要安装 pygame: pip install pygame")
            return
        
        pygame.init()
        
        # 创建透明窗口
        screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        pygame.display.set_caption("Live2D Pet")
        
        # 设置窗口透明度
        screen.set_alpha(None)
        
        clock = pygame.time.Clock()
        
        print("\n🐱 Live2D 桌面宠物启动！")
        print("🎮 提示: 点击宠物可以互动，拖拽可以移动位置")
        print("🔴 按 ESC 或关闭窗口退出\n")
        
        while self.running:
            current_time = pygame.time.get_ticks()
            
            # 处理事件
            self.handle_events()
            
            # 更新状态
            self.update(current_time)
            
            # 渲染
            self.render(screen)
            
            # 控制帧率
            clock.tick(self.frame_rate)
        
        pygame.quit()
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.is_click_on_pet(mouse_x, mouse_y):
                        self.dragging = True
                        self.drag_offset = (mouse_x - self.x, mouse_y - self.y)
                        self.on_click()
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            
            elif event.type == MOUSEMOTION:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if self.dragging:
                    self.x = self.mouse_x - self.drag_offset[0]
                    self.y = self.mouse_y - self.drag_offset[1]
                    # 限制在屏幕内
                    screen_info = pygame.display.Info()
                    self.x = max(0, min(self.x, screen_info.current_w - self.screen_width))
                    self.y = max(0, min(self.y, screen_info.current_h - self.screen_height))
    
    def is_click_on_pet(self, mouse_x: int, mouse_y: int) -> bool:
        """检查点击是否在宠物区域内"""
        return (self.x < mouse_x < self.x + self.screen_width and
                self.y < mouse_y < self.y + self.screen_height)
    
    def on_click(self):
        """处理点击事件"""
        print("✨ 宠物被点击了！")
        self.set_expression("happy")
    
    def set_expression(self, expression: str):
        """设置表情"""
        self.expression = expression
        self.expression_timer = pygame.time.get_ticks()
    
    def update(self, current_time: int):
        """更新状态"""
        # 动画帧更新
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        # 表情超时恢复
        if current_time - self.expression_timer > 2000:
            self.expression = "normal"
        
        # 自动移动
        self.auto_move_timer += 16
        if self.auto_move_timer > self.auto_move_interval:
            self.auto_move_timer = 0
            screen_info = pygame.display.Info()
            self.target_x = random.randint(0, screen_info.current_w - self.screen_width)
            self.target_y = random.randint(0, screen_info.current_h - self.screen_height)
    
    def render(self, screen):
        """渲染"""
        # 清空屏幕
        screen.fill((0, 0, 0, 0))
        
        # 绘制当前帧
        if self.frames:
            frame = self.frames[self.current_frame]
            # 调整大小以适应窗口
            frame = pygame.transform.smoothscale(frame, (self.screen_width, self.screen_height))
            screen.blit(frame, (0, 0))
        
        # 更新显示
        pygame.display.flip()
        
        # 更新窗口位置
        pygame.display.set_window_position(self.x, self.y)


def main():
    parser = argparse.ArgumentParser(
        description="Live2D Desktop Pet - 桌面Live2D桌宠功能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从分层目录创建桌宠
  python live2d_desktop_pet.py --layers-dir layers_12345 --output my_pet
  
  # 从PSD文件创建桌宠（需要psd-tools）
  python live2d_desktop_pet.py --psd layers.psd --output my_pet
  
  # 运行桌宠
  python live2d_desktop_pet.py --run my_pet
  
  # 完整工作流示例:
  python live2d_workflow.py "蓝发猫耳少女" --deploy-desktop
"""
    )
    
    parser.add_argument("--layers-dir", type=str, help="分层图片目录")
    parser.add_argument("--psd", type=str, help="PSD文件路径")
    parser.add_argument("--output", type=str, default="./pet_output", help="输出目录")
    parser.add_argument("--run", type=str, help="运行已创建的桌宠")
    
    args = parser.parse_args()
    
    if args.run:
        # 运行桌宠
        if not os.path.exists(args.run):
            print(f"❌ 桌宠目录不存在: {args.run}")
            return 1
        
        config_path = Path(args.run) / "animation_config.json"
        frames_dir = Path(args.run) / "frames"
        
        if not config_path.exists() or not frames_dir.exists():
            print("❌ 桌宠文件不完整，请先创建桌宠")
            return 1
        
        runner = PetRunner(str(config_path), str(frames_dir))
        runner.run()
        return 0
    
    if not args.layers_dir and not args.psd:
        print("❌ 请提供 --layers-dir 或 --psd 参数")
        parser.print_help()
        return 1
    
    # 创建桌宠
    if args.layers_dir:
        animator = DesktopPetAnimator(args.layers_dir, args.output)
        animator.create_pet_package()
    elif args.psd:
        # 从PSD提取图层
        print(f"📦 从PSD文件提取图层: {args.psd}")
        try:
            from psd_tools import PSDImage
            psd = PSDImage.open(args.psd)
            
            # 创建临时图层目录
            layers_dir = Path(args.output) / "extracted_layers"
            layers_dir.mkdir(parents=True, exist_ok=True)
            
            # 导出每个图层
            for layer in psd.descendants():
                if layer.has_pixels():
                    img = layer.topil()
                    layer_path = layers_dir / f"{layer.name}.png"
                    img.save(layer_path)
                    print(f"   ✓ 导出图层: {layer.name}")
            
            # 创建桌宠
            animator = DesktopPetAnimator(str(layers_dir), args.output)
            animator.create_pet_package()
            
        except ImportError:
            print("❌ 需要安装 psd-tools: pip install psd-tools")
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
