# 题 29：哪些属性会继承？如何强制继承/不继承？

## 面试官可能怎么问

- 字号颜色会继承吗？
- margin 继承吗？
- inherit / initial / unset / revert？

## 口述结构（90 秒）

1. **会继承**多见于文字相关：`color`、`font-*`、`line-height`、`text-align` 等
2. **不继承**：盒模型（`width/margin/padding/border`）、定位、背景、`display` 等
3. 关键字：`inherit` 强制跟父；`initial` 回初始；`unset` 能继则继否则 initial；`revert` 回到用户代理/用户样式
4. 写组件别假设「父 margin 会传下来」；链接 `a` 常有 UA 色要显式设

## 参考答案

### 1. 会不会继承？（面试清单）

**通常继承（文字类）**

- `color`、`font-family`、`font-size`、`font-weight`、`font-style`
- `line-height`、`letter-spacing`、`word-spacing`
- `text-align`、`text-indent`、`visibility`（注意：和 `display` 不同）
- `list-style`、`cursor`、`direction` 等

**通常不继承（盒子 / 视觉盒）**

- `width` / `height`、`margin`、`padding`、`border`
- `background*`、`display`、`position`、`float`、`overflow`
- `top/right/bottom/left`、`z-index`

口诀：**「长什么样的字」常继；「盒子怎么摆、多大」一般不继。**

```css
body { color: #222; font-family: system-ui, sans-serif; line-height: 1.5; }
/* 子元素文字默认跟着走；但每个盒子的 margin 要自己设 */
```

### 2. margin 继承吗？

**不继承。**  
子元素 `margin` 默认是 `0`（视元素而定），不会变成父的 `margin: 24px`。

```css
.card { margin: 24px; }
.card p { /* margin 不会自动 24px */ }
```

间距策略：父子用父 `padding`；兄弟用父 `gap` 或各自 margin（注意合并，见 BFC 题）。

### 3. inherit / initial / unset / revert

```css
.btn {
  font: inherit;      /* 按钮跟正文字体，而不是 UA 按钮字体 */
  color: inherit;
}

.isolate {
  color: initial;     /* 该属性回到 CSS 规范初始值（如 color 常是 canvasText/黑） */
}

.quiet {
  color: unset;       /* 若属性可继承 → 等价 inherit；否则 → initial */
  display: unset;     /* display 不可继承 → initial（通常 inline） */
}

.ua-like {
  all: revert;        /* 尽量回到浏览器默认样式层，慎用 all */
}
```

| 关键字 | 含义 | 何时用 |
| --- | --- | --- |
| `inherit` | 强制用父计算值 | 按钮/表单跟正文、强制传 `color` |
| `initial` | 规范初始值 | 清掉某属性的「怪值」 |
| `unset` | 可继则 inherit，否则 initial | 快捷重置单个属性 |
| `revert` | 回到级联里更早来源（常像 UA） | 撤掉作者样式影响 |
| `revert-layer` | 回到上一个 `@layer` | 设计系统分层时 |

### 4. 业务落地

```css
/* 全局文字靠继承 */
body { font-family: "PingFang SC", sans-serif; color: #1f1f1f; }

/* 链接有 UA 蓝色+下划线，要显式 */
a { color: #1677ff; text-decoration: none; }
a:hover { text-decoration: underline; }

/* 组件根不要让标题样式污染内部按钮 */
.panel h3 { font-size: 18px; }
.panel .btn { font: inherit; font-size: 14px; }
```

## 可能追问

- `a` 的颜色？→ UA 样式权重大，常需作者显式写；只设 `body{color}` 不够。
- `all: unset`？→ 一次清掉几乎所有属性，影响面极大，组件里慎用。
- `visibility` 继承而 `display` 不？→ 对，隐藏子树时 `visibility:hidden` 仍占位且子可再 `visible`。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
