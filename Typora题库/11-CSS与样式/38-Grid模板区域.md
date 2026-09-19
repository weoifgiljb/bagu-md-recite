# 题 38：Grid 的 template-areas / fr / minmax 怎么讲？

## 面试官可能怎么问

- fr 是什么？
- minmax(0,1fr) 为什么？
- areas 排版？

## 口述结构（90 秒）

1. **`fr`**：把「剩余空间」按份数分，不是固定 px
2. **`minmax(min, max)`**：轨道有上下限；`minmax(0, 1fr)` 防止内容最小尺寸把 `1fr` 撑破
3. **`grid-template-areas`**：用ASCII图画后台壳（头/侧/主/脚），子项 `grid-area: 名字`
4. 响应式：窄屏改 areas 字符串或改列定义；卡片墙用 `auto-fill`/`auto-fit` + `minmax`

## 参考答案

### 1. fr 是什么？（回答该问）

`fr`（fraction）表示**剩余空间的份数**。

```css
.grid {
  display: grid;
  grid-template-columns: 200px 1fr 2fr;
  /* 先拿走 200px，剩下的按 1:2 分给后两列 */
}
```

多个 `fr` 按比例分；可和 `px`/`%`/`auto` 混用。`1fr` 常等价思路于「吃剩余」，但和 Flex 的 `flex:1` 分配算法不同（面试说「都是分剩余，细节别混」即可）。

### 2. 为什么写 `minmax(0, 1fr)`？（回答该问）

默认情况下，网格轨道的最小尺寸受**内容最小尺寸**影响（类似 Flex 的 `min-width: auto`）。长单词、不换行表格、大图会把 `1fr` 列撑出滚动条或撑破布局。

```css
.layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  /* 右侧：最小可以收到 0，最大吃剩余 → 溢出在列内处理 */
}
.main {
  min-width: 0;      /* 双保险，子项也常要 */
  overflow: auto;    /* 内容在主区滚，而不是撑开整页 */
}
```

口诀：**要让 `1fr` 真能缩，就给轨道 `minmax(0,1fr)`，子项必要时 `min-width:0`。**

### 3. areas 排版（回答该问）

```css
.page {
  display: grid;
  min-height: 100vh;
  grid-template-columns: 240px minmax(0, 1fr);
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header"
    "side   main"
    "footer footer";
  gap: 0;
}
.header { grid-area: header; }
.side   { grid-area: side; }
.main   { grid-area: main; }
.footer { grid-area: footer; }

@media (max-width: 768px) {
  .page {
    grid-template-columns: minmax(0, 1fr);
    grid-template-areas:
      "header"
      "main"
      "side"
      "footer";
  }
}
```

同一行字符串里，名字相同的单元格会合并成跨列/跨行区域；`.` 表示空单元格。

### 4. 响应卡片墙（加分）

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
  gap: 16px;
}
```

`auto-fill` vs `auto-fit`：都是自动数列；`auto-fit` 会把空轨道塌掉让实列拉伸，`auto-fill` 保留空轨道——面试能点一句即可。

## 可能追问

- `dense`？→ `grid-auto-flow: dense` 回填空洞，注意视觉顺序与 DOM 顺序可能不一致（无障碍）。
- `subgrid`？→ 子网格继承父轨道对齐，复杂表头/卡片内对齐很好用，视浏览器支持。
- `fr` 和 `%`？→ `%` 相对网格容器；`fr` 相对**分完非 fr 轨道后的剩余**。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
