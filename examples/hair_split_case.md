# 头发拆分案例

## 拆分原则
- 确保运动时不发生穿模
- 每层独立可控
- 预留足够的遮挡区域

## 拆分建议

### 前发
- hair_front_01（刘海最前，独立物理）
- hair_front_02（刘海中间层）
- hair_front_03（刘海最后层）

### 侧发
- hair_side_l_01（左测发上半）
- hair_side_l_02（左测发下半，独立物理）
- hair_side_r_01（右测发上半）
- hair_side_r_02（右测发下半，独立物理）

### 后发
- hair_back_01（后发最上）
- hair_back_02（后发中间）
- hair_back_03（后发最下，独立物理）

## 绑定建议
- 前发：绑定 ParamAngleZ
- 侧发：绑定 ParamAngleX
- 后发：物理为主
