# 动漫少女角色设定文档

## 基本信息

| 项目 | 内容 |
|------|------|
| **角色名称** | 待定（可由用户指定） |
| **风格** | 可爱萌系 |
| **分辨率** | 4096×4096 (4K) |
| **用途** | Live2D VTuber |

---

## 角色外观设定

### 👩 头部特征

| 部位 | 详细描述 |
|------|----------|
| **发型** | 长发，及腰长度 |
| **发色** | 粉色渐变（发根浅粉，发梢深粉） |
| **发质** | 柔顺丝滑，有光泽感 |
| **刘海** | 空气刘海，微卷 |
| **发饰** | 可选：蝴蝶结发夹、星星发饰 |

### 👀 面部特征

| 部位 | 详细描述 |
|------|----------|
| **眼型** | 大眼，杏眼，可爱型 |
| **瞳色** | 粉紫色渐变 |
| **眼妆** | 自然眼影，下眼睑高光 |
| **睫毛** | 浓密卷翘，自然色 |
| **眉毛** | 自然弯曲，浅粉色 |

### 👄 嘴部特征

| 部位 | 详细描述 |
|------|----------|
| **唇形** | 小巧可爱，樱桃小嘴 |
| **唇色** | 自然粉嫩 |
| **表情** | 微笑，露出贝齿 |

---

## 👗 服装设定

### JK 制服套装

| 部位 | 详细描述 |
|------|----------|
| **上装** | 白色短袖衬衫，领口有红色丝带领结 |
| **下装** | 深蓝色百褶裙，及膝长度 |
| **配饰** | 红色丝带领结、校徽胸针 |
| **鞋子** | 黑色玛丽珍鞋，白色短袜 |

### 可选配饰

- 🎒 学生书包
- 📚 课本/笔记本
- 🌸 樱花胸针
- ⌚ 手表

---

## 🎨 Live2D 分层建议

### 必需图层（按 Draw Order 排序）

```
1. 背景（可选，通常透明）
2. hair_back_01        # 后发
3. body_back           # 身体后部
4. arm_back_l          # 左臂后
5. arm_back_r          # 右臂后
6. skirt_01            # 裙子
7. body_front          # 身体前部
8. arm_front_l         # 左臂前
9. arm_front_r         # 右臂前
10. neck               # 脖子
11. face_base          # 脸部基础
12. face_shadow        # 脸部阴影
13. eye_l_white        # 左眼白
14. eye_r_white        # 右眼白
15. eye_l_iris         # 左眼虹膜
16. eye_r_iris         # 右眼虹膜
17. eye_l_pupil        # 左眼瞳孔
18. eye_r_pupil        # 右眼瞳孔
19. eye_l_highlight    # 左眼高光
20. eye_r_highlight    # 右眼高光
21. eyebrow_l          # 左眉
22. eyebrow_r          # 右眉
23. nose               # 鼻子
24. mouth_base         # 嘴巴基础
25. mouth_a            # 嘴型 A (啊)
26. mouth_i            # 嘴型 I (伊)
27. mouth_u            # 嘴型 U (呜)
28. mouth_e            # 嘴型 E (诶)
29. mouth_o            # 嘴型 O (哦)
30. hair_front_01      # 前发
31. hair_front_02      # 刘海
32. accessories        # 配饰
```

---

## 🎭 动态部件建议

### 可动部件

| 部件 | 动画类型 | 参数建议 |
|------|----------|----------|
| **头发** | 摇摆、飘动 | ParamAngleX/Y/Z, 物理模拟 |
| **眼睛** | 眨眼、视线移动 | ParamEyeLOpen/ROpen, ParamEyeBallX/Y |
| **嘴巴** | 口型切换 | ParamMouthOpenY, ParamMouthForm |
| **眉毛** | 表情变化 | ParamBrowLY/RY, ParamBrowLAngle/RAngle |
| **身体** | 呼吸、转身 | ParamBodyAngleX/Y, 呼吸动画 |

### 物理参数建议

```json
{
  "hair": {
    "gravity": 0.5,
    "air_resistance": 0.85,
    "spring_constant": 0.3,
    "damping": 0.7
  },
  "accessories": {
    "gravity": 0.3,
    "air_resistance": 0.9,
    "spring_constant": 0.2,
    "damping": 0.8
  }
}
```

---

## 📊 质量标准

### 图像质量要求

- ✅ 分辨率: 4096×4096 (4K)
- ✅ 颜色模式: RGB
- ✅ 文件格式: PSD
- ✅ 图层分离: 清晰可分
- ✅ 边缘处理: 锐利无模糊
- ✅ 透明度: 正确设置

### Live2D 兼容性

- ✅ 混合模式: 仅 Normal
- ✅ 图层命名: 英文规范
- ✅ 图层结构: 合理分组
- ✅ 遮挡关系: 正确处理
- ✅ 文件大小: < 50MB

---

## 🚀 下一步操作

1. **配置 API 密钥** - 设置 ARK_API_KEY 环境变量
2. **生成立绘** - 使用 Seedream 5.0 生成高质量图像
3. **PSD 分层** - 按照上述分层建议进行分层
4. **质量检查** - 使用 QA 工具检查文件
5. **Cubism 导入** - 导入到 Live2D Cubism
6. **绑定设置** - 设置参数和物理

---

## 💡 提示词模板

### Seedream 5.0 完整提示词

```
anime girl, cute kawaii style, beautiful face, big expressive eyes,
long flowing pink hair, soft pink gradient hair, hair strands detailed,
wearing JK school uniform, white blouse, navy blue pleated skirt,
red ribbon tie, school bag accessory,
slender figure, elegant pose, standing pose,
perfect for Live2D rigging, clean layer separation,
isolated character on white background, easy to rig,
sharp clean lines, vibrant colors, ultra detailed,
masterpiece, award-winning quality, professional artwork,
4K resolution, high quality render, anime art style,
soft lighting, detailed facial features, sparkling eyes
```

### 质量增强关键词

```
4K, 8K, ultra detailed, masterpiece, award-winning,
professional artwork, high quality, best quality,
sharp focus, vibrant colors, perfect anatomy
```

### Live2D 专用关键词

```
perfect for Live2D rigging,
clean layer separation,
isolated character,
white background,
easy to rig,
sharp clean lines
```

---

**创建时间**: 2026-05-20  
**版本**: v3.0  
**状态**: 等待 API 配置
