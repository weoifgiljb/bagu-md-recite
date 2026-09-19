# 题 34：min() / max() / clamp() 有什么用？

## 面试官可能怎么问

- 流体字号怎么写？
- 和媒体查询关系？
- 宽度上限？

## 口述结构（90 秒）

1. `min()` 取更小、`max()` 取更大；`clamp(MIN, VAL, MAX)` = `max(MIN, min(VAL, MAX))`
2. **流体字号**：`clamp(最小 rem, 中间用 vw/公式, 最大 rem)`，字随屏宽平滑变
3. **宽度上限**：`width: min(100% - 边距, 1080px)` 居中容器，少写一层 max-width
4. 能少写部分断点，但布局大改（侧栏显隐、栅格列数）仍要媒体查询 / 容器查询

## 参考答案

### 1. 三个函数分别干什么

```css
width: min(100%, 400px);   /* 不超过 400，且不超过父宽 */
width: max(50%, 200px);    /* 至少 200，且至少半宽 */
font-size: clamp(14px, 2vw, 20px); /* 14～20 之间跟 2vw 走 */
```

`clamp(MIN, PREFERRED, MAX)` 要求 `MIN ≤ MAX`，否则行为怪异（按规范会交换等），面试写清楚三个参数顺序。

### 2. 流体字号（回答「流体字号怎么写」）

```css
:root {
  /* 下限可读 + 中间随视口 + 上限防桌面过大 */
  --step-0: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --step-1: clamp(1.25rem, 1rem + 1.2vw, 2rem);
}
h1 { font-size: var(--step-1); line-height: 1.25; }
body { font-size: var(--step-0); }
```

更精确的线性插值（已知两断点）：  
`preferred ≈ 最小字号 + (最大-最小) * (100vw - 最小视口) / (最大视口 - 最小视口)`，常写成 `clamp(1.25rem, 2vw + 1rem, 2rem)` 这种「vw + rem」组合。

无障碍：最小不要低于约 `1rem`（或产品规定的可读下限）；用户放大字体时 rem 方案比死 px 更友好。

### 3. 宽度上限（回答「宽度上限」）

```css
.wrap {
  width: min(100% - 32px, 1080px); /* 左右各留约 16px，且不超过 1080 */
  margin-inline: auto;
}
/* 等价老写法：
.wrap { width: 100%; max-width: 1080px; padding-inline: 16px; box-sizing: border-box; margin-inline: auto; }
*/
```

卡片栅格列宽也可用：`grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));`（注意 `min()` 包一层避免 minmax 溢出）。

### 4. 和媒体查询的关系（回答该追问）

| 用 clamp/min/max | 仍用 @media / @container |
| --- | --- |
| 字号、间距、容器宽度连续变化 | 侧栏从下变右、导航汉堡化、列数从 1→3 等结构变化 |
| 少几个「只改 font-size」的断点 | 关键布局断点、打印样式、`prefers-reduced-motion` |

可以组合：媒体查询里改 clamp 的三个参数或改 CSS 变量。

```css
.hero { font-size: clamp(1.5rem, 1rem + 2vw, 3rem); }
@media (max-width: 600px) {
  .nav { display: none; } /* 结构变化，不是 clamp 能替代的 */
}
```

## 可能追问

- 和 `calc()` 组合？→ 可以：`clamp(1rem, calc(1rem + 2vw), 2rem)`；很多浏览器里 clamp 第二参直接写 `1rem + 2vw` 也行。
- 容器单位 `cqw`？→ 跟 `@container` 搭配做「跟组件宽」的流体，而不是跟视口。
- 性能？→ 计算很轻；真正成本仍是布局本身。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
