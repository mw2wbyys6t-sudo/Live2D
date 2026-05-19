# Live2D 角色立绘生成提示词

本文件包含用于生成高质量 Live2D 角色立绘的提示词模板和参数配置。

---

## 质量级别预设

| 级别 | 步数 | CFG | 描述 |
|------|------|-----|------|
| **Draft** | 15 | 5.5 | 快速预览，质量一般 |
| **Standard** | 25 | 7.0 | 标准质量，平衡速度与效果 |
| **High** | 35 | 7.5 | 高质量，细节丰富 |
| **Ultra** | 50 | 8.0 | 超高质量，8K 级别细节 |

---

## 分辨率预设

| 预设 | 尺寸 | 适用场景 |
|------|------|----------|
| square-512 | 512×512 | 小图标、缩略图 |
| square-768 | 768×768 | 标准头像 |
| square-1024 | 1024×1024 | 高质量头像 |
| square-1280 | 1280×1280 | 超高清头像 |
| portrait-512x768 | 512×768 | 小尺寸半身像 |
| portrait-768x1024 | 768×1024 | 标准半身像 |
| portrait-1024x1536 | 1024×1536 | 高质量半身像 |

---

## 风格类型

### 1. Anime (动漫风格)
```
anime style, beautiful detailed anime artwork, anime aesthetic, sharp clean lines, vibrant colors, studio quality animation cel
```
**负面提示词**: 3d, realistic, photo, photograph, text, watermark

### 2. Realistic (写实风格)
```
hyperrealistic, photorealistic, highly detailed, lifelike, cinematic lighting, professional photography
```
**负面提示词**: cartoon, anime, drawing, sketch, text, watermark

### 3. Cel-shaded (赛璐珞风格)
```
cel shaded, flat colors, clean outlines, 2D animation style, Toon shader, bold lines
```
**负面提示词**: realistic, 3d render, photorealistic, text, watermark

### 4. Watercolor (水彩风格)
```
watercolor painting, soft brush strokes, watercolor wash, delicate colors, artistic texture
```
**负面提示词**: digital art, 3d render, photorealistic, text, sharp edges

### 5. Pixel-art (像素风格)
```
pixel art, retro 8-bit style, pixel perfect, nostalgic gaming aesthetic, crisp pixels
```
**负面提示词**: smooth, anti-aliased, 3d, realistic, text

### 6. 3D Render (3D渲染)
```
3D render, blender, octane render, realistic materials, ray tracing, cinematic
```
**负面提示词**: 2d, flat, cartoon, hand-drawn, text, watermark

### 7. Oil Painting (油画风格)
```
oil painting, brush strokes, classic art style, textured canvas, masterful technique
```
**负面提示词**: digital art, 3d render, photorealistic, text, watermark

---

## 提示词模板

### 模板 1: 基础 VTuber 角色
```
可爱的二次元动漫女孩，正面朝向，半身像，粉色长发双马尾，蓝色大眼睛，水手服，可爱的表情，白色背景
```

### 模板 2: 兽耳 VTuber (猫耳)
```
可爱的动漫女孩，正面半身像，猫耳，金色长发，绿色眼睛，洛丽塔风格连衣裙，甜美的微笑，白色背景
```

### 模板 3: 兽耳 VTuber (兔耳)
```
可爱的兔耳女孩，正面朝向，粉色短发，红色眼睛，偶像风格服装，开心的表情，纯白色背景
```

### 模板 4: 优雅角色
```
优雅的二次元女性角色，正面朝向，深蓝色中长发，紫色眼睛，黑色连衣裙，平静的表情，精致的妆容，白色背景
```

### 模板 5: Q版角色
```
Q版可爱动漫女孩，正面朝向，粉色短发，红色大眼睛，校服风格，开心的表情，白色背景，简单干净的线条
```

### 模板 6: 男性角色
```
帅气的二次元男性角色，正面半身像，黑色短发，蓝色眼睛，休闲服装，自信的微笑，白色背景
```

---

## 角色元素清单

### 头发选项
- 短发、中长发、长发
- 双马尾、单马尾
- 卷发、直发
- 渐变发色、挑染
- 刘海样式：齐刘海、斜刘海、无刘海

### 眼睛选项
- 眼睛大小：大眼睛、中等眼睛、小眼睛
- 眼睛颜色：蓝色、绿色、紫色、金色、棕色、红色、粉色、琥珀色
- 眼睛样式：圆形、杏仁形、下垂眼、锐利眼

### 服装选项
- 水手服、连衣裙、洛丽塔、校服、休闲装
- 偶像装、女仆装、魔法少女装
- 哥特风、朋克风、和风、古风

### 配件选项
- 兽耳：猫耳、兔耳、狐耳、狼耳、熊耳
- 头饰：发夹、发带、帽子、皇冠
- 尾巴：猫尾、兔尾、狐尾
- 翅膀：天使翅膀、恶魔翅膀
- 其他：眼镜、项链、耳环、围巾

### 表情选项
- 微笑、开心大笑、平静、害羞、惊讶、生气、悲伤、眨眼

---

## 高质量关键词

### 画质提升
```
高质量，高分辨率，8K，4K，精致的细节，超详细，锐利清晰
```

### 艺术风格
```
插画风格，动漫风格，专业插画，工作室质量，获奖作品
```

### Live2D 适配
```
适合 Live2D 建模，清晰分层，纯色背景，易于绑定，干净的线条
```

---

## 负面提示词基础
```
low quality, blurry, distorted, pixelated, ugly, deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, missing limb, floating limbs, disconnected limbs, malformed hands, long neck, bad proportions, watermark, text, signature, logo, cropped, out of frame
```

---

## 完整提示词示例

### 示例 1: 高质量动漫角色
```
anime style, beautiful detailed anime artwork, cute anime girl, front view, half body, pink long hair twin tails, big blue eyes, sailor uniform, sweet smile, white background, 8K, ultra detailed, masterpiece, award-winning, professional artwork, perfect for Live2D rigging, clean layer separation, isolated character, solid background
```

### 示例 2: 超高质量兽耳角色
```
anime style, beautiful detailed anime artwork, cute cat girl, front facing, half body portrait, golden long hair, green eyes, lolita dress, happy expression, pure white background, 8K resolution, ultra detailed, masterpiece quality, stunning visuals, perfect for Live2D rigging, clean layers, easy to animate
```

### 示例 3: Q版角色
```
chibi anime style, cute chibi girl, front view, pink short hair, big red eyes, school uniform, cheerful expression, white background, high quality, clean lines, simple design, perfect for Live2D chibi rigging
```
