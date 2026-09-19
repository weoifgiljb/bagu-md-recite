# 题 21：margin 垂直塌陷（合并）是什么？

## 面试官可能怎么问

- 父子 margin 合并？
- 兄弟合并规则？
- 怎么防止？

## 口述结构（90 秒）

1. 相邻块级盒在同一 BFC 里，垂直 margin 可能合并成一个
2. 兄弟：大致取较大者（同号）；父子：子的 `margin-top` 可能「穿出」父
3. 防：父建 BFC、父加 padding/border、用 flex `gap`、改用 padding
4. 水平 margin 不合并

## 参考答案

### 1. 父子 margin 合并？（对应第 1 问）

**现象**：父没有 border/padding，子写 `margin-top: 20px`，结果空隙出现在父**外面**，父背景没把这 20px 包住。

**原因**：满足条件时，子的顶 margin 与父的顶 margin 合并，视觉上像子「顶穿」父。

**遇见问题 → 怎么办**
```css
/* 方案 A：给父一点 padding 或 border，打断合并 */
.section { padding-top: 1px; }          /* 或 padding-top: 16px 直接当间距 */
.section { border-top: 1px solid transparent; }

/* 方案 B：父开 BFC */
.section { display: flow-root; }

/* 方案 C：子改用父的 padding，子 margin-top:0 */
.section { padding-top: 20px; }
.section > .title { margin-top: 0; }
```

### 2. 兄弟合并规则？（对应第 2 问）

- 两块相邻：`margin-bottom: 24px` 与 `margin-top: 16px` → 实际空隙通常是 **24px**（同号取大），不是 40。
- 一正一负：大致相加（如 20 + (-8) = 12）。
- 设计稿「对不齐」很多是合并，不是浏览器算错。

### 3. 怎么防止？（对应第 3 问）

| 手段 | 适用 |
| --- | --- |
| 父 `display: flow-root` / `overflow: auto` | 隔开父子合并 |
| 父 `padding` / `border` | 简单粗暴 |
| Flex/Grid + `gap` | 新布局首选，不靠垂直 margin 拼 |
| 只保留一侧 margin | 约定「只用 margin-bottom」 |
| 间距改 padding | 组件内部更稳 |

```css
/* 推荐现代写法 */
.stack { display: flex; flex-direction: column; gap: 16px; }
.stack > * { margin: 0; }
```

**业务例子**：标题与段落间距总少一截 → 先怀疑合并；组件库里用 `gap` 或统一 padding。

## 可能追问

- 空块 margin？→ 空块自己的上下 margin 也可能合并，出现「空白塌掉」。
- Flex 项之间？→ Flex/Grid 格式化上下文不走普通块级那套合并。
- 水平方向？→ 左右 margin 不合并。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
