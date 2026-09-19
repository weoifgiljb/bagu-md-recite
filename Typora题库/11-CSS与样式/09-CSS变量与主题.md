# 题 9：CSS 变量怎么做主题切换？和预处理器变量差在哪？

## 面试官可能怎么问

- `--*` 自定义属性会继承吗？作用域怎么控？
- 暗色主题怎么切？局部主题呢？
- `var(--x, fallback)` 怎么用？
- 和 Less/Sass 变量、Tailwind token 怎么配合？
- 运行时改主题会不会很卡？

## 口述结构（90 秒）

1. CSS 变量是运行时的：继承、可被 JS/媒体查询改
2. 设计 token 挂在 `:root` / `[data-theme]`；组件用 `var(--color-bg)`
3. 切换：改 `document.documentElement` 的 class 或 `data-theme`
4. Less 变量编译期死掉，适合算色；运行时主题用 CSS 变量
5. 局部暗色：只在容器上覆盖变量，不必整页切换

## 参考答案

### 1. 基础写法

```css
:root {
  --color-bg: #ffffff;
  --color-text: #111111;
  --color-primary: #1677ff;
  --radius: 8px;
}
[data-theme="dark"] {
  --color-bg: #141414;
  --color-text: #f5f5f5;
  --color-primary: #3c89ff;
}
body {
  background: var(--color-bg);
  color: var(--color-text);
}
.button {
  background: var(--color-primary, #1677ff); /* 回退 */
  border-radius: var(--radius);
}
```

```js
document.documentElement.dataset.theme =
  document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
```

也可跟系统：

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* 用户未强制浅色时跟随系统 */
    --color-bg: #141414;
    --color-text: #f5f5f5;
  }
}
```

### 2. 作用域与局部主题

```css
.sidebar {
  --color-bg: #0f172a;   /* 只影响侧栏及其后代的 var 引用 */
  --color-text: #e2e8f0;
  background: var(--color-bg);
  color: var(--color-text);
}
```

变量会继承；子元素 `var(--color-bg)` 取最近定义。面试金句：**「就近覆盖 + 继承」**。

### 3. 和 Less/Sass 的差别

| | 预处理器变量 | CSS 变量 |
| --- | --- | --- |
| 时机 | 编译期 | 运行时 |
| JS 切换主题 | 难（要多份 CSS） | 改几个变量即可 |
| 算色/循环 | 强 | 弱一些（可 `@property` 增强） |
| 配合 | 编出默认 token | 运行时覆盖 token |

实践：Less 生成默认 `:root { --color-primary: ... }`，暗色只覆盖变量表。

### 4. 遇到问题怎么办

**问题 A：切主题后有的组件颜色没变**

1. 查是否写死 `#fff`/`rgb` 而非 `var`。  
2. 第三方库是否用自己的主题 API（Ant Design `ConfigProvider` / CSS 变量模式）。  
3. 画布/Canvas、图标 font 色是否独立。  
4. 修法：把硬编码换成 token；或包一层覆盖类。

**问题 B：闪白（FOUC）**

1. 在首屏 HTML 内联一小段脚本，按 `localStorage` 先设 `data-theme`，再加载应用。  
2. 或内联关键 CSS 变量，避免等异步 CSS。

**问题 C：动画主题色**

```css
@property --color-primary {
  syntax: '<color>';
  inherits: true;
  initial-value: #1677ff;
}
.button { transition: --color-primary .2s; } /* 视支持度 */
```

不支持时退化为直接切换。

**问题 D：性能**

- 改 `:root` 几个变量通常可接受；避免每帧 JS 改大量内联样式。  
- 大面积阴影/滤镜与主题无关的成本别算到变量头上。

**业务例子**：整站暗色改 `data-theme`；文档预览区单独暗色沙箱只覆盖预览容器变量。

## 可能追问

- 变量能用在 media 外面控制断点吗？→ 媒体查询条件里不能拿自定义属性当断点值（历史限制），断点仍写死或容器查询。  
- 短横线命名？→ `--color-bg` 一类 token 名，避免和浏览器冲突。  
- 与 Tailwind？→ Tailwind 也可映射到 CSS 变量做运行时主题。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
