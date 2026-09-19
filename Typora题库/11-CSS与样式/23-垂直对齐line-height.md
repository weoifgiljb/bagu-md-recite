# 题 23：行高、vertical-align 和文字垂直居中？

## 面试官可能怎么问

- line-height 设数字和 px 区别？
- 图片和下方空隙？
- 单行垂直居中？

## 口述结构（90 秒）

1. `line-height` 控制行框高度；**无单位数字**按元素自身 `font-size` 相乘且可继承，`px`/`em` 是算死的长度
2. `img` 默认按基线（baseline）对齐，行框里会留「幽灵空隙」；用 `display:block` 或改 `vertical-align` 消掉
3. **单行**可用 `line-height = height`；多行/图标+文字优先 `flex` + `align-items:center`
4. 图标字体、小图标对齐常调 `vertical-align` 或直接上 flex，别死磕魔法数

## 参考答案

### 1. line-height：数字 vs px（必答）

```css
.parent { font-size: 16px; line-height: 1.5; }   /* 继承的是「因子 1.5」 */
.child  { font-size: 24px; } /* 行高 = 24 * 1.5 = 36 */

.parent2 { font-size: 16px; line-height: 24px; } /* 继承的是「24px」这个长度 */
.child2  { font-size: 24px; } /* 行高仍是 24px，容易挤 */
```

| 写法 | 继承到子元素时 | 推荐 |
| --- | --- | --- |
| `line-height: 1.5`（数字） | 子按**自己字号 × 1.5** | 正文首选 |
| `line-height: 150%` / `1.5em` | 先按**父字号**算出 px 再继承 | 易踩坑，少用 |
| `line-height: 24px` | 固定 24px | 按钮单行尚可，正文慎用 |

步骤：定正文节奏 → 全局 `body { line-height: 1.5; }` → 标题单独调，不要到处写死 px。

### 2. 图片下方空隙怎么消

现象：`img` 和文字同一行时，图片底部和容器底边之间多出几像素空隙。

原因：行内替换元素默认 `vertical-align: baseline`，基线下方还要给字母「尾巴」（如 g、y）留空，于是图片底下空一截。

```css
/* 方案 A：块级，脱离行内对齐（最常用） */
.card > img { display: block; width: 100%; height: auto; }

/* 方案 B：改垂直对齐 */
.card > img { vertical-align: middle; /* 或 bottom / top */ }

/* 方案 C：父级取消行框影响 */
.card { font-size: 0; } /* 旧招；记得子文字再设回字号 */
.card { line-height: 0; } /* 同上，副作用大，慎用 */
```

验收：DevTools 看 img 底边是否贴齐容器；旁边有文字时优先 B 或 flex，别乱 `font-size:0`。

### 3. 单行 / 多行垂直居中

**单行文字（固定高度按钮）**

```css
.btn {
  height: 40px;
  line-height: 40px; /* 单行 ≈ 盒高 */
  padding: 0 16px;
  /* 不要再加上下 padding，否则会撑破 */
}
```

注意：一旦换行或中英混排行高异常，这个技巧就失效。

**图标 + 文字 / 多行（推荐）**

```css
.item {
  display: flex;
  align-items: center; /* 交叉轴居中 */
  gap: 8px;
  min-height: 40px;
}
.item__icon { width: 20px; height: 20px; flex: 0 0 auto; }
```

**纯 CSS 表格法（了解）**：父 `display:table-cell; vertical-align:middle;` —— 老项目能见，新项目用 flex。

### 4. vertical-align 速记

只对**行内 / 行内块 / 表格单元格**生效，对普通块级兄弟无效。

```css
img, .icon { vertical-align: middle; }
sup { vertical-align: super; }
```

业务例子：列表项左侧 SVG 图标 + 文案，直接 `display:flex; align-items:center`，比调 `vertical-align` 稳。

## 可能追问

- 幽灵空白节点 / strut？→ 行内格式化上下文里，浏览器为行高生成的匿名文字支柱，导致图片「悬空」。
- `line-height: normal`？→ 看字体，约 1.2，不可控，组件里建议显式数字。
- 绝对定位垂直居中？→ `top:50%; transform:translateY(-50%)` 或 flex/grid，和 line-height 是两套题。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
