# 题 36：CSS 变量作用域、回退与主题切换细节？

## 面试官可能怎么问

- 变量会继承吗？
- 局部主题怎么做？
- 和 Less 变量一起用？

## 口述结构（90 秒）

1. 自定义属性会**继承**；子元素 `var(--x)` 取祖先链上最近定义
2. `var(--c, #000)` 写回退；还可 `var(--a, var(--b, #ccc))` 多层
3. **局部主题**：只在侧栏/卡片根设一套变量，不影响主区；全局主题切 `html[data-theme]`
4. Less/Sass 编译期常量 + 运行时 CSS 变量：构建出默认 token，运行时只改 CSS 变量做换肤

## 参考答案

### 1. 会不会继承？（回答该问）

会。自定义属性是继承属性：子元素没定义时沿用父值；谁定义就近覆盖。

```css
:root { --brand: #1677ff; --text: #1f1f1f; }
.card { color: var(--text); border-color: var(--brand); }
.card.danger { --brand: #ff4d4f; } /* 只影响该卡片及其子孙的 var(--brand) */
```

注意：`var(--brand)` 的「计算」发生在使用处；改祖先变量会让子孙重算（可动画的前提见 `@property`）。

### 2. 回退

```css
.btn {
  background: var(--btn-bg, var(--brand, #1677ff));
  padding: var(--btn-pad, 8px 16px);
}
```

未定义或无效时用第二个参数。调试时可在 DevTools 看 Computed 是否落到回退。

### 3. 局部主题怎么做？（回答该问）

**全局换肤**

```css
:root, [data-theme="light"] {
  --bg: #fff;
  --fg: #111;
  --border: #e5e5e5;
}
[data-theme="dark"] {
  --bg: #141414;
  --fg: #f5f5f5;
  --border: #303030;
}
body {
  background: var(--bg);
  color: var(--fg);
}
```

```js
document.documentElement.dataset.theme = "dark"; // 只切根节点
```

**局部暗色侧栏（不影响主内容）**

```css
.sidebar {
  --bg: #0f172a;
  --fg: #e2e8f0;
  --brand: #38bdf8;
  background: var(--bg);
  color: var(--fg);
}
.sidebar a { color: var(--brand); }
.main {
  /* 继续用 :root 的 --bg/--fg，不被 sidebar 污染 */
}
```

关键：变量定义在「主题根」上，使用方都写 `var(--*)`，不要把颜色写死在叶子上。

### 4. 和 Less 变量一起用？（回答该问）

| | Less/Sass 变量 | CSS 变量 |
| --- | --- | --- |
| 时机 | 编译期 | 运行时 |
| 换肤 | 难（要编多份或 CSS 变量桥接） | 适合 |
| 计算/循环 | 强 | 弱一些（逐步增强） |

工程实践：

```less
// tokens.less —— 编译期默认值灌进 CSS 变量
@brand: #1677ff;
:root {
  --brand: @brand;
  --brand-hover: darken(@brand, 6%);
}
```

运行时主题只覆盖 `--brand` 等 CSS 变量；Less 的 mixin/嵌套继续服务组件结构。Ant Design 一类也是「Less 编译 + 设计 token」，动态主题越来越多走 CSS 变量。

媒体查询里也能改：

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #141414;
    --fg: #f5f5f5;
  }
}
```

## 可能追问

- `@property`？→ 注册类型后部分属性可过渡/动画（如颜色、长度）。
- 变量能用在媒体查询条件里吗？→ 一般不能当 `@media` 的断点值；但可以在 media **块内**改变量。
- 和 Shadow DOM？→ 外部变量可穿透继承进 shadow（除非在 host 重置）。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
