# VTuber 马尾角色 PSD 分层规划方案

**角色类型**: VTuber
**头发类型**: 马尾
**配件**: 头饰
**生成日期**: 2026-05-14

---

## 一、完整图层结构

### 层级顺序（从顶层到底层）

#### 1. 头发最前层（Hair Front Most）
```
hair_front_most_01    # 马尾最前端的发束
hair_front_most_02    # 马尾前侧发束
hair_front_most_03    # 马尾根部
```

#### 2. 头饰层（Head Accessory）
```
accessory_base        # 头饰底座
accessory_detail_01   # 头饰细节1
accessory_detail_02   # 头饰细节2
accessory_front       # 头饰前部装饰
```

#### 3. 前发/刘海层（Hair Bangs）
```
hair_bangs_01         # 刘海第一层（前）
hair_bangs_02         # 刘海第二层（中）
hair_bangs_03         # 刘海第三层（后）
hair_side_l_01        # 左侧刘海
hair_side_r_01        # 右侧刘海
```

#### 4. 脸部细节层（Face Details）
```
eyebrow_l_01          # 左眉毛
eyebrow_r_01          # 右眉毛
eye_l_white           # 左眼白
eye_l_iris            # 左眼虹膜
eye_l_pupil           # 左眼瞳孔
eye_l_highlight       # 左眼高光
eye_r_white           # 右眼白
eye_r_iris            # 右眼虹膜
eye_r_pupil           # 右眼瞳孔
eye_r_highlight       # 右眼高光
nose_01               # 鼻子
mouth_base            # 嘴巴基础
mouth_a               # 嘴型 A
mouth_i               # 嘴型 I
mouth_u               # 嘴型 U
mouth_e               # 嘴型 E
mouth_o               # 嘴型 O
blush_l_01            # 左脸颊红晕
blush_r_01            # 右脸颊红晕
```

#### 5. 脸部基础层（Face Base）
```
face_base             # 脸部基础形状
face_shadow           # 脸部阴影
ear_l_01              # 左耳朵
ear_r_01              # 右耳朵
```

#### 6. 马尾层（Twintails / Pigtails）
```
twintail_l_01         # 左马尾第一段
twintail_l_02         # 左马尾第二段
twintail_l_03         # 左马尾第三段
twintail_l_tip        # 左马尾发尾
twintail_r_01         # 右马尾第一段
twintail_r_02         # 右马尾第二段
twintail_r_03         # 右马尾第三段
twintail_r_tip        # 右马尾发尾
```

#### 7. 后发层（Hair Back）
```
hair_back_01          # 后发第一层
hair_back_02          # 后发第二层
hair_back_03          # 后发第三层
hair_back_neck        # 颈部后发
```

#### 8. 身体层（Body）
```
neck                  # 脖子
body_base             # 身体基础
clothes_collar        # 衣领
clothes_front         # 衣服前部
clothes_back          # 衣服后部（可见部分）
clothes_detail_01     # 衣服细节1
clothes_detail_02     # 衣服细节2
arm_l_01              # 左臂
arm_r_01              # 右臂
hand_l_01             # 左手
hand_r_01             # 右手
```

#### 9. 背景层（Background）
```
background_base       # 背景基础
background_detail     # 背景细节
```

---

## 二、图层分组建议

### 分组 1: 头发组（Hair Group）
```
├── Hair Group
│   ├── hair_front_most (马尾最前)
│   ├── hair_bangs (刘海)
│   ├── hair_side (侧发)
│   ├── twintail_l (左马尾)
│   ├── twintail_r (右马尾)
│   └── hair_back (后发)
```

### 分组 2: 脸部组（Face Group）
```
├── Face Group
│   ├── face_base (脸型)
│   ├── eye_l (左眼)
│   ├── eye_r (右眼)
│   ├── eyebrows (眉毛)
│   ├── nose (鼻子)
│   ├── mouth (嘴巴)
│   ├── blush (红晕)
│   └── ears (耳朵)
```

### 分组 3: 身体组（Body Group）
```
├── Body Group
│   ├── neck (脖子)
│   ├── clothes (衣服)
│   ├── arms (手臂)
│   └── hands (手)
```

### 分组 4: 配件组（Accessory Group）
```
├── Accessory Group
│   ├── accessory_base (头饰底座)
│   └── accessory_details (头饰细节)
```

---

## 三、Cubism 绑定建议

### 3.1 Warp Deformer（变形器）设置

#### 脸部变形器
```
Deformer: Face Deformer
├── face_base
├── face_shadow
├── eye_l
├── eye_r
└── mouth
```

#### 前发变形器
```
Deformer: Hair Bangs Deformer
├── hair_bangs_01
├── hair_bangs_02
├── hair_bangs_03
├── hair_side_l_01
└── hair_side_r_01
```

#### 马尾变形器
```
Deformer: Twintail L Deformer
├── twintail_l_01
├── twintail_l_02
├── twintail_l_03
└── twintail_l_tip

Deformer: Twintail R Deformer
├── twintail_r_01
├── twintail_r_02
├── twintail_r_03
└── twintail_r_tip
```

### 3.2 Rotation Deformer（旋转器）设置

#### 耳朵旋转器
```
Deformer: Ear L Rotation
├── ear_l_01
└── rotation: -10° ~ 10°

Deformer: Ear R Rotation
├── ear_r_01
└── rotation: -10° ~ 10°
```

#### 马尾根部旋转器
```
Deformer: Twintail L Root Rotation
├── twintail_l_01
└── rotation: -30° ~ 30° (跟随 ParamAngleZ)

Deformer: Twintail R Root Rotation
├── twintail_r_01
└── rotation: -30° ~ 30° (跟随 ParamAngleZ)
```

---

## 四、参数设置建议

### 4.1 基础参数

| 参数名 | 说明 | 范围 | 建议 |
|--------|------|------|------|
| ParamAngleX | 左右转头 | -30 ~ 30 | 跟随脸部 |
| ParamAngleY | 上下点头 | -20 ~ 20 | 跟随脸部 |
| ParamAngleZ | 左右歪头 | -25 ~ 25 | 跟随脸部 |
| ParamEyeLOpen | 左眼开合 | 0 ~ 1 | 眨眼 |
| ParamEyeROpen | 右眼开合 | 0 ~ 1 | 眨眼 |
| ParamMouthOpenY | 嘴巴开合 | 0 ~ 1 | 说话 |
| ParamMouthForm | 嘴型变化 | 0 ~ 1 | 口型 |

### 4.2 表情参数

| 参数名 | 说明 | 范围 |
|--------|------|------|
| ParamSmile | 微笑 | 0 ~ 1 |
| ParamWinkL | 左眼眨眼 | 0 ~ 1 |
| ParamWinkR | 右眼眨眼 | 0 ~ 1 |
| ParamSurprise | 惊讶 | 0 ~ 1 |
| ParamAnger | 生气 | 0 ~ 1 |
| ParamBlush | 脸红 | 0 ~ 1 |

### 4.3 头发参数

| 参数名 | 说明 | 范围 | 绑定对象 |
|--------|------|------|----------|
| ParamHairFront | 前发摆动 | 0 ~ 1 | hair_bangs |
| ParamTwintailL | 左马尾摆动 | 0 ~ 1 | twintail_l |
| ParamTwintailR | 右马尾摆动 | 0 ~ 1 | twintail_r |
| ParamHairBack | 后发摆动 | 0 ~ 1 | hair_back |

---

## 五、物理设置建议

### 5.1 马尾物理参数

#### 左马尾物理
```
Physics: Twintail L Physics
- 重力 (Gravity): 0.6
- 风力 (Wind): 0.2
- 回复力 (Restitution): 0.5
- 阻尼 (Damping): 0.85
- 物理点数量: 10
- 建议: 独立物理，响应头部运动
```

#### 右马尾物理
```
Physics: Twintail R Physics
- 重力 (Gravity): 0.6
- 风力 (Wind): 0.2
- 回复力 (Restitution): 0.5
- 阻尼 (Damping): 0.85
- 物理点数量: 10
- 建议: 独立物理，响应头部运动
```

### 5.2 刘海物理参数

```
Physics: Hair Bangs Physics
- 重力 (Gravity): 0.4
- 风力 (Wind): 0.15
- 回复力 (Restitution): 0.6
- 阻尼 (Damping): 0.9
- 物理点数量: 5
- 建议: 轻微物理，避免遮挡眼睛
```

### 5.3 后发物理参数

```
Physics: Hair Back Physics
- 重力 (Gravity): 0.7
- 风力 (Wind): 0.25
- 回复力 (Restitution): 0.45
- 阻尼 (Damping): 0.8
- 物理点数量: 8
- 建议: 中等物理，增加动态感
```

---

## 六、Draw Order 建议

### 绘制顺序（从后到前）

1. `background_base` ← 最底层
2. `hair_back_03`
3. `hair_back_02`
4. `hair_back_01`
5. `hair_back_neck`
6. `body_base`
7. `neck`
8. `clothes_back`
9. `clothes_front`
10. `arm_l_01`
11. `arm_r_01`
12. `hand_l_01`
13. `hand_r_01`
14. `face_base` ← 脸部基础
15. `face_shadow`
16. `ear_l_01`
17. `ear_r_01`
18. `mouth_base` ← 嘴巴
19. `mouth_a/i/u/e/o`
20. `nose_01`
21. `eye_l_white` ← 眼睛
22. `eye_l_iris`
23. `eye_l_pupil`
24. `eye_l_highlight`
25. `eye_r_white`
26. `eye_r_iris`
27. `eye_r_pupil`
28. `eye_r_highlight`
29. `blush_l_01`
30. `blush_r_01`
31. `eyebrow_l_01`
32. `eyebrow_r_01`
33. `hair_side_l_01` ← 侧发
34. `hair_side_r_01`
35. `hair_bangs_03` ← 刘海
36. `hair_bangs_02`
37. `hair_bangs_01`
38. `accessory_base` ← 头饰
39. `accessory_detail_01`
40. `accessory_detail_02`
41. `accessory_front`
42. `twintail_l_03` ← 马尾
43. `twintail_l_02`
44. `twintail_l_01`
45. `twintail_l_tip`
46. `twintail_r_03`
47. `twintail_r_02`
48. `twintail_r_01`
49. `twintail_r_tip`
50. `hair_front_most_03` ← 马尾最前
51. `hair_front_most_02`
52. `hair_front_most_01`
53. `background_detail` ← 背景细节

---

## 七、注意事项

### 7.1 遮挡问题
- ✅ 马尾摆动时不能遮挡脸部
- ✅ 刘海不能完全遮住眼睛
- ✅ 头饰不能遮挡重要面部特征

### 7.2 对称性
- ✅ 左眼和右眼需要严格对称
- ✅ 左马尾和右马尾需要对称
- ✅ 左右侧发需要对称

### 7.3 预留空间
- ✅ 脸部需要预留转头空间
- ✅ 马尾需要预留摆动空间
- ✅ 头发层之间需要预留遮挡重叠空间

---

## 八、工作流程建议

### Phase 1: PSD 准备
1. 导入立绘
2. 按照上述结构分层
3. 检查图层命名
4. 验证对称性

### Phase 2: Cubism 导入
1. 导入 PSD
2. 检查 Draw Order
3. 设置 Mesh
4. 创建 Deformers

### Phase 3: 绑定
1. 绑定脸部参数
2. 绑定眼睛参数
3. 绑定嘴巴参数
4. 设置物理

### Phase 4: 测试
1. 测试转头效果
2. 测试眨眼效果
3. 测试马尾物理
4. 检查遮挡问题

### Phase 5: 导出
1. 导出 .moc3
2. 导出纹理图集
3. 测试模型效果

---

**生成完成！** 

如果你有角色立绘图片，可以上传给我，我可以帮你进行更具体的分析和微调。
