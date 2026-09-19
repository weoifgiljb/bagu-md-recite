# 题 19：px / em / rem / vw / vh / % 怎么选？

## 面试官可能怎么问

- em 和 rem 区别？
- 移动端用哪套？
- % 的参照是谁？

## 口述结构（90 秒）

1. px 绝对 CSS 像素；% 相对父；em 相对**当前元素**字体；rem 相对**根元素**字体
2. vw/vh 相对视口；`vmin/vmax` 取短边/长边
3. 适配：rem 方案或 vw；流体字号常用 `clamp`
4. 细边框、阴影偏移多用 px；注意用户字体缩放与无障碍

## 参考答案

### 1. em 和 rem 区别？（对应第 1 问）

| 单位 | 参照 | 坑 |
| --- | --- | --- |
| `em` | 当前元素 `font-size`（嵌套会叠乘） | 父 1.2em、子再 1.2em → 复合放大 |
| `rem` | 根元素（`html`）`font-size` | 更稳，组件间距常用 |
| `px` | CSS 像素 | 不随根字号变（仍受浏览器缩放影响） |

```css
html { font-size: 16px; }
.card { font-size: 1.25rem; }     /* 20px */
.card .tip { padding: 0.5em; }  /* 相对 .card 的 20px → 10px */
.card .tip { padding: 0.5rem; } /* 相对根 16px → 8px */
```

### 2. 移动端用哪套？（对应第 2 问）

常见三套（面试说清取舍即可）：

1. **rem 方案**：按设计稿（如 375）设 `html` 字号，或用 flexible/`postcss-pxtorem`。
2. **vw 方案**：把稿宽当 100vw，直接写 `width: 10.67vw` 等；或 PostCSS `px-to-viewport`。
3. **现代流体**：布局用 Flex/Grid + `%`；字号 `clamp(14px, 2.5vw, 18px)`。

```css
.title {
  font-size: clamp(16px, 2.2vw, 22px);
}
```

**细线边框**：继续 `1px solid`，不要盲目转 rem 出 `0.02667rem` 一类难读值。

### 3. % 的参照是谁？（对应第 3 问）

- `width: %` → 含块（父）的**宽度**。
- `height: %` → 父必须有**明确高度**，否则常当 auto（见题 20）。
- `padding/margin` 的 % → 通常相对含块**宽度**（含上下 padding 也按宽算，易踩坑）。
- `translate(% )` → 相对**自身**宽高。

**遇见问题 → 怎么办**
| 现象 | 处理 |
| --- | --- |
| 字号一层层暴涨 | 少嵌套 em，改 rem |
| 大屏字过大 | `clamp(min, preferred, max)` 封顶 |
| 设计 375 对不齐 | 统一一种适配方案，别 rem + vw 混算同一尺寸 |

**业务例子**：设计稿 375；间距/字号走 rem 或 clamp；1px 分割线用 px；全屏背景可用 `100%` / `100dvh`。

## 可能追问

- 窗口变大字过大？→ `clamp` 设上限。
- em 复合？→ 多层 em 叠乘，rem 更稳。
- `vmin`？→ 取 vw/vh 中较小者，正方形适配常用。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
