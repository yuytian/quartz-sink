# 清石石英洗手池 — 设计系统文档

## 项目概述

- **项目名称**: 清石石英洗手池 (QingShi Quartz Wash Basin)
- **产品类型**: 石英石卫浴制造商官网 (B2B/B2C 混合)
- **目标受众**: 国内外卫浴经销商、工程采购商、家装设计师
- **设计定位**: 高端、专业、天然、可信赖

## 设计决策依据 (UI/UX Pro Max)

| 数据来源 | 匹配内容 | 应用 |
|---------|---------|------|
| products.csv #51 | Construction/Architecture → Minimalism + 3D | 产品展示采用极简风格 + 质感表现 |
| products.csv #161 | Home Decoration → Minimalism + Natural | 暖色调石材纹理背景 |
| colors.csv #84 | Architecture/Interior → #171717 + #A16207 | 主色岩板黑 + 古铜金点缀 |
| colors.csv #161 | Home Decoration → #78716C + #D97706 | 暖灰背景辅助色调 |
| typography.csv #25 | Chinese Simplified → Noto Sans SC | 全站中文字体 |
| typography.csv #5 | Minimal Swiss → Inter (拉丁字符) | 拉丁字符/数字字体 |
| landing.csv #31 | Feature-Rich Showcase → 产品网格 + 特性 | 产品区布局 |
| landing.csv #33 | Trust & Authority → 认证 + 数据 | 信任区布局 |

## 设计标记 (Design Tokens)

### 色彩系统

```
Primary (岩板黑):     #171717  →  正文、标题、深色背景
Secondary (暖灰):     #525252  →  辅助文字
Accent (古铜金):      #A16207  →  强调色、标签、CTA 高亮
Accent Light:         #CA8A04  →  亮态强调
Accent Soft:          #FEF3C7  →  柔和强调背景

Background:           #FAFAFA  →  页面主背景
Background Warm:      #FAF5F2  →  暖色区块背景
Surface:              #FFFFFF  →  卡片/面板
Surface Muted:        #F5F0EB  →  次级面板背景
Border:               #E8E4E0  →  分割线/边框
Border Strong:        #D6D3D1  →  强调边框

Text Primary:         #171717  →  主要文字
Text Secondary:       #525252  →  次要文字
Text Muted:           #8C8C8C  →  辅助/禁用文字
Text Inverse:         #FFFFFF  →  深色底反白文字
```

### 字体系统

| 层级 | 字体 | 字号 | 字重 | 行高 |
|------|------|------|------|------|
| Hero Title | Noto Sans SC | 60px (3.75rem) | 700 | 1.15 |
| Section Title | Noto Sans SC | 48px (3rem) | 700 | 1.3 |
| Card Title | Noto Sans SC | 18px (1.125rem) | 700 | 1.3 |
| Body | Noto Sans SC | 16px (1rem) | 400 | 1.75 |
| Small/Caption | Noto Sans SC | 14px (0.875rem) | 400/500 | 1.6 |
| Label | Noto Sans SC | 14px (0.875rem) | 600 | 1.5 |

### 间距系统 (8px Grid)

```
4px  →  微小间距 (图标与文字)
8px  →  紧凑间距 (标签内边距)
12px →  小间距
16px →  标准内边距
24px →  卡片内边距 / 组件间距
32px →  区块内间距
40px →  中段间距
48px →  大段间距
64px →  区块间距
80px →  页面区块间距 (移动端)
128px → 页面区块间距 (桌面端)
```

### 圆角

```
4px  →  小型元素 (标签、徽章)
8px  →  按钮、输入框
12px →  卡片
16px →  大型卡片
24px →  英雄区产品展示
```

### 阴影层级

```
sm:  0 1px 2px rgba(0,0,0,0.05)           →  微妙分层
md:  0 4px 6px rgba(0,0,0,0.07)           →  悬停卡片
lg:  0 10px 15px rgba(0,0,0,0.08)         →  弹出层
xl:  0 20px 25px rgba(0,0,0,0.1)          →  模态框/英雄区
```

## 页面结构

1. **导航栏** — 固定顶部，毛玻璃效果
2. **Hero** — 全屏主视觉 + 产品展示 + 核心数据
3. **产品中心** — 6 款产品卡片网格
4. **工厂实力** — 照片墙 + 4 大优势
5. **数据面板** — 4 项关键数据
6. **工艺制程** — 8 步工艺流程
7. **资质认证** — 6 项认证展示
8. **CTA** — 联系方式 + 行动号召
9. **页脚** — 链接 + 版权

## UX 合规检查清单

- [x] 颜色对比度 ≥ 4.5:1 (WCAG AA)
- [x] 所有交互元素 ≥ 44px 触控区域
- [x] 可见的焦点环 (3px #A16207)
- [x] 语义化 HTML5 标签
- [x] 图片描述性 alt 文本
- [x] 支持 prefers-reduced-motion
- [x] 移动优先响应式设计
- [x] 导航键盘可操作
- [x] 表单标签可见
- [x] Skip-to-content 链接
- [x] SVG 图标 (无 emoji 作为图标)
- [x] 滚动动画不阻塞交互
- [x] 移动端无水平滚动
