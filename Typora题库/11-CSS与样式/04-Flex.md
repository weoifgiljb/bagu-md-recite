# 题 4：Flex 布局核心概念？常见坑怎么排？

## 面试官可能怎么问

- 主轴、交叉轴、`flex-direction` 关系？
- `flex:1` 是什么意思？`flex-grow/shrink/basis`？
- 为什么子项缩不下去、把布局撑破？
- `align-items` / `justify-content` / `align-self` 怎么记？
- 和 Grid 怎么选？

## 口述结构（90 秒）

1. Flex 是一维布局：先定主轴方向，再分配剩余空间
2. 容器：`display:flex`、`flex-direction`、`justify-content`、`align-items`、`flex-wrap`、`gap`
3. 项目：`flex` 简写、`align-self`、`order`（慎用）
4. 高频坑：`min-width:auto` 导致缩不下去 → `min-width:0`；长文本要省略
5. 一维用 Flex，二维网格用 Grid；能 `gap` 就少用 margin 拼间距

## 参考答案

### 1. 轴与对齐（口述别乱）

```css
.row {
  display: flex;
  flex-direction: row;          /* 主轴水平；column 则主轴垂直 */
  justify-content: space-between; /* 主轴：空间怎么分 */
  align-items: center;            /* 交叉轴：默认 stretch */
  gap: 12px;
  flex-wrap: wrap;                /* 不够就换行 */
}
```

- `justify-*` → 主轴；`align-*` → 交叉轴。  
- `flex-direction: column` 后，原来的「左右」常要改用 `align-items` 才能水平居中——面试爱挖这个。

### 2. `flex` 简写（常考）

| 写法 | 常见含义（口述版） |
| --- | --- |
| `flex: 1` | 可增长可收缩，basis 常按 `0%`/`0` 理解，用来「分剩余空间」 |
| `flex: auto` | 按内容 basis，再参与伸缩 |
| `flex: none` | 不增不缩，尺寸跟内容/自己的宽高 |
| `flex: 0 0 200px` | 固定 200px 侧栏 |

```css
.side { flex: 0 0 200px; }
.main { flex: 1; min-width: 0; } /* 中间自适应必写 min-width:0 */
```

更细：`flex-grow` 分「多出来的空间」；`flex-shrink` 空间不够谁被挤；`flex-basis` 分配前的基准。

### 3. 遇到问题怎么办

**坑 A：子项内容把 Flex 容器撑破（搜不到省略）**

1. 现象：中间栏长文件名/URL，把侧栏挤没或出现横向滚动。  
2. 原因：Flex 项默认 `min-width: auto`，不能小于内容最小宽度。  
3. 处理：

```css
.main { flex: 1; min-width: 0; }
.main .title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space:nowrap;
}
```

4. 垂直方向同理：列布局用 `min-height: 0`，否则内部 `overflow:auto` 滚不动。

**坑 B：`align-items:center` 后等高卡片没了**

- 默认 `stretch` 才能等高；居中会取消拉伸。等高+内容垂直居中：外层 stretch，内层再 Flex 居中。

**坑 C：换行后最后一行不对齐**

- `justify-content:space-between` + wrap 时最后一行可能左右拉开。可用 Grid 或接受/改用 `flex-start` + `gap`。

**坑 D：嵌套滚动区**

```css
.page { display: flex; flex-direction: column; height: 100vh; }
.head { flex: none; }
.body { flex: 1; min-height: 0; overflow: auto; }
```

### 4. 和 Grid 怎么选

- 导航、工具栏、左右结构、沿一条轴分配 → **Flex**。  
- 海报墙、整页分区、行列交叉对齐 → **Grid**。  
- 两者可嵌套：外 Grid 搭骨架，内 Flex 排按钮。

**业务例子**：顶栏 Logo | 搜索 | 头像：左右 `flex:none`，搜索 `flex:1; min-width:0`。

## 可能追问

- `flex-basis:0` vs `auto`？→ `0` 更「均分剩余」；`auto` 更看内容尺寸再分。
- `order`？→ 只改视觉顺序，Tab/读屏仍按 DOM，无障碍场景慎用。
- `gap` 老浏览器？→ 极老环境才用 margin 模拟；现在面试优先讲 `gap`。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
