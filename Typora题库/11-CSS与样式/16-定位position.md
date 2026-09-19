# 题 16：position 各值区别？containing block 是什么？

## 面试官可能怎么问

- static/relative/absolute/fixed/sticky 差在哪？
- absolute 相对谁定位？
- fixed 在 transform 父级下为啥怪？

## 口述结构（90 秒）

1. static 默认；relative 占位偏移；absolute 相对最近定位祖先；fixed 通常相对视口
2. sticky：在阈值内像 relative，越界后像 fixed（吸顶）
3. absolute/fixed 的参照是 containing block；祖先有 transform/filter/perspective 等时，fixed 可能「吸」在该祖先上
4. 弹层、吸顶表头、锚点导航是高频场景

## 参考答案

### 1. 五个值差在哪？（对应第 1 问）

| 值 | 是否脱离普通流 | 参照 / 行为 |
| --- | --- | --- |
| `static` | 否 | 默认，top/left 无效 |
| `relative` | 否（占位保留） | 相对自己原来的位置偏移 |
| `absolute` | 是 | 相对最近的「定位祖先」（非 static） |
| `fixed` | 是 | 通常相对视口；见第 3 问例外 |
| `sticky` | 特殊 | 滚动到阈值前跟流，之后粘住 |

```css
.badge { position: absolute; top: -4px; right: -4px; } /* 父要 relative */
.header { position: sticky; top: 0; z-index: 10; }
.mask { position: fixed; inset: 0; }
```

### 2. absolute 相对谁定位？（对应第 2 问）

- 找最近的 `position` 不为 `static` 的祖先，作为 containing block。
- 找不到就相对 **初始 containing block**（可理解为整页）。
- **实践**：要角标贴卡片，父级写 `position: relative`（或 sticky/absolute 等），子级 `absolute`。

**遇见问题 → 怎么办**
1. 角标跑到页面角落：父级没有定位 → 给卡片加 `position: relative`。
2. 被父级 `overflow:hidden` 裁掉：弹层改挂到 `body`（Vue Teleport / React Portal）。

### 3. fixed 在 transform 父级下为啥怪？（对应第 3 问）

- 规范：祖先若形成特定 containing block（常见：`transform` ≠ none、`filter`、`perspective`、`will-change` 相关、`contain` 等），`fixed` 会相对**该祖先**定位，而不是视口。
- 表现：滚动页面时「fixed」侧栏跟着父级动，像 absolute。

**遇见问题 → 怎么办**
1. DevTools 选中 fixed 元素，看是谁在当 containing block。
2. 去掉祖先无必要的 `transform`，或把弹层/导航 **Teleport 到 body**。
3. 吸顶失效时同步检查：祖先 `overflow: hidden/auto`、没有滚动空间、`top` 未设。

**业务例子**：表头 `sticky; top:0`；模态框 `fixed` + Teleport，避开带 `transform` 的动画容器。

## 可能追问

- sticky 不生效？→ 祖先 overflow 不是 visible、自身无 top、父级高度不够滚、或 flex 子项缺 `align-self` 等。
- z-index？→ 一般要非 static（及新层叠上下文）才比较；同级比 z-index，跨上下文先比父级。
- `inset: 0`？→ 等价 top/right/bottom/left 都为 0。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
