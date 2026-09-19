# 题 39：Flex 还有哪些常考坑？（加深）

## 面试官可能怎么问

- flex:1 展开？
- 为什么内容把盒子撑破？
- gap 与 margin？

## 口述结构（90 秒）

1. **`flex:1`** 常见展开为 `flex-grow:1; flex-shrink:1; flex-basis:0%`（让份额按 grow 分，而不是先按内容宽度再分）
2. **撑破**：默认 `min-width:auto`（或纵向 `min-height:auto`）按内容最小尺寸，子项缩不下去 → 设 `min-width:0` / `overflow:hidden` 并配合 `flex-shrink`
3. **间距**：优先容器 `gap`；旧浏览器才用子项 margin；`gap` 不额外产生「首尾外边距」 entanglements
4. 其它：`align-items` 默认 stretch；换行要 `flex-wrap`；`order` 只改视觉勿乱改无障碍顺序

## 参考答案

### 1. `flex:1` 展开成什么？（回答该问）

```css
.item { flex: 1; }
/* 常见等价意图： */
.item { flex-grow: 1; flex-shrink: 1; flex-basis: 0%; }
```

对比：

| 写法 | 直觉 |
| --- | --- |
| `flex: 1` / `1 1 0%` | 忽略内容宽度差异，按份数分剩余（更「均分」） |
| `flex: auto`（`1 1 auto`） | 先按内容/宽高，再分配剩余 |
| `flex: none`（`0 0 auto`） | 不伸不缩 |

搜索栏经典：

```css
.bar { display: flex; gap: 8px; align-items: center; }
.bar .logo, .bar .actions { flex: none; }
.bar .search {
  flex: 1;
  min-width: 0; /* 见下 */
}
.bar input {
  width: 100%;
  box-sizing: border-box;
}
```

### 2. 为什么内容把盒子撑破？（回答该问）

现象：中间 `flex:1` 的区域里有长文本/表格/大图，整行被撑出横向滚动，或把旁边按钮挤没。

原因：Flex 项默认 `min-width: auto`，最小不能小于内容固有最小宽度，**shrink 失效**。

处理步骤：

```css
.pane {
  flex: 1;
  min-width: 0;     /* 关键：允许小于内容固有宽度 */
  overflow: auto;   /* 溢出在pane内滚 */
}
.pane .ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

纵轴同理（列方向 Flex）：用 `min-height: 0`。Grid 的 `1fr` 列见题 38 的 `minmax(0,1fr)`。

### 3. gap 与 margin（回答该问）

```css
/* 推荐 */
.row { display: flex; gap: 12px 16px; } /* 行间距 列间距 */

/* 老写法 */
.row > * + * { margin-left: 16px; } /* 要自己处理换行、RTL、首尾 */
```

| | gap | 子项 margin |
| --- | --- | --- |
| 换行 | 两维间距一起对 | 易在换行边出乱 margin |
| 首尾 | 不在容器边缘多出空隙 | 常要 :first-child 清 |
| 兼容 | 现代 OK | 极旧环境兜底 |

`margin: auto` 在 Flex 里仍可用来「把剩余空间吃掉」做左右推挤（如左边一组、右边一组），和 `gap` 可并存。

### 4. 其它高频坑（口述可带一句）

- `align-items: stretch` 默认；要垂直居中改 `center`。
- 要换行：`flex-wrap: wrap`，否则 `flex-basis`/`width` 再小也可能挤在一行。
- `inline-flex` 与文字基线对齐有时出缝，图片加 `display:block`。

## 可能追问

- `flex-basis: 0` 和 `auto`？→ `0` 更均分；`auto` 看 width/内容。
- `order`？→ 只改视觉顺序，Tab/读屏仍跟 DOM；无障碍场景慎用。
- 负数 `flex-grow`？→ 无效；shrink 可为小数调节压缩比例。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
