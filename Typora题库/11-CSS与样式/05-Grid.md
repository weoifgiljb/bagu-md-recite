# 题 5：Grid 布局怎么讲？和 Flex 区别？

## 面试官可能怎么问

- `fr`、`minmax`、`repeat`、`auto-fill/auto-fit` 是什么？
- `grid-template-areas` 适合什么场景？
- 为什么常写 `minmax(0, 1fr)`？
- 二维布局为什么更适合 Grid？
- 网格溢出、子项撑破轨道怎么处理？

## 口述结构（90 秒）

1. Grid 是二维：同时控行和列
2. 定义轨道：`grid-template-columns/rows`，用 `fr` 分剩余空间，`minmax` 防撑破
3. 放置：线号、`span`、或 `grid-template-areas` 语义化
4. 响应式：`repeat(auto-fill, minmax(240px, 1fr))` 做卡片墙
5. 和 Flex：一维 vs 二维；后台壳常用 Grid，组件内条带用 Flex

## 参考答案

### 1. 基础骨架

```css
.layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  grid-template-rows: 56px 1fr;
  grid-template-areas:
    "header header"
    "side   main";
  height: 100vh;
  gap: 0;
}
.header { grid-area: header; }
.side   { grid-area: side; overflow: auto; }
.main   { grid-area: main; min-width: 0; overflow: auto; }
```

### 2. 关键概念（面试要会口述）

| 概念 | 一句话 |
| --- | --- |
| `fr` | 剩余空间的份数，不是固定 px |
| `minmax(min, max)` | 轨道最小/最大约束 |
| `minmax(0, 1fr)` | 允许轨道收到 0，避免内容最小宽度把 `1fr` 撑破 |
| `repeat(3, 1fr)` | 三等列 |
| `auto-fill` | 尽量多塞轨道，可能留空轨 |
| `auto-fit` | 会把空轨塌掉，让有内容的列拉伸更满 |

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}
```

### 3. 放置方式

```css
.item { grid-column: 1 / 3; }      /* 占两列 */
.item { grid-column: span 2; }
.item { grid-area: main; }         /* 配合 areas */
```

对齐：容器上 `justify-items` / `align-items`；单个用 `justify-self` / `align-self`。整块内容在格子里居中可用 `place-items: center`。

### 4. 遇到问题怎么办

**坑 A：`1fr` 列被长内容撑出横向滚动**

1. 现象：主内容区表格/代码块把侧栏挤没。  
2. 处理：列写成 `minmax(0, 1fr)`，内容区 `min-width:0; overflow:auto`。

```css
grid-template-columns: 240px minmax(0, 1fr);
.main { min-width: 0; overflow: auto; }
```

**坑 B：隐式行把高度撑乱**

- 只定义了列，行是隐式 `auto`。固定视口布局要显式 `grid-template-rows`，滚动放在内部区域。

**坑 C：子元素 `height:100%` 不生效**

- 确认网格行有确定高度（如 `1fr` 在固定总高容器里）；子要 `min-height:0` 才能内部滚动。

**坑 D：和绝对定位弹层**

- Grid 项也能当定位祖先；弹层仍建议挂 `body`，避免被 `transform` 的格子影响。

### 5. 和 Flex 对比（收尾金句）

- **一条轴分配**（顶栏、面包屑+按钮）→ Flex。  
- **行列同时对齐**（管理后台壳、杂志排版、卡片墙）→ Grid。  
- 可以嵌套，不要为用 Grid 而 Grid。

**业务例子**：中后台 `侧栏 + 顶栏 + 内容` 用 areas；列表页卡片墙用 `auto-fill + minmax`。

## 可能追问

- `dense`？→ 自动填充前面空洞，可能打乱视觉源序，无障碍要谨慎。
- `subgrid`？→ 子网格对齐父轨道，支持渐好，面试提概念即可。
- Grid 能画重叠层吗？→ 同一格子多项目叠放 + `z-index`。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
