# 题 13：Less 是什么？和 CSS / Sass 差在哪？

## 面试官可能怎么问

- 为什么还要用 Less？
- 变量、嵌套、mixin 怎么用？
- Less 和 Sass 选型？

## 口述结构（90 秒）

1. Less 是 CSS 预处理器：变量、嵌套、mixin、运算，**构建期**编译成普通 CSS
2. 浏览器不直接吃 `.less`；Vite/Webpack/`lessc` 转译，开发态可 HMR
3. 相对 Sass：语法更接近 CSS、上手快；Sass（Dart Sass）能力/生态更强，看团队存量
4. 新项目主题更爱 **CSS 变量**；Less 仍常见于后台/老项目的 token 体系

## 参考答案

### 1. 为什么还要用 Less？（对应第 1 问）

- **痛点**：纯 CSS 里颜色、间距、圆角到处复制，改主题要全局搜；重复布局片段难复用。
- **Less 解决**：编译期变量 + mixin + 嵌套，把设计 token 收口到少数文件。
- **什么时候可以不用**：全新项目若已全面 Tailwind / 纯 CSS 变量 + PostCSS，可以不引入 Less；**存量 Vue/后台**里全局 Less 仍很常见，面试要能讲清。

### 2. 变量、嵌套、mixin 怎么用？（对应第 2 问）

```less
// variables.less
@color-brand: #2563eb;
@space-md: 16px;

// mixins.less
.flex-center(@gap: 8px) {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: @gap;
}

// page.less
@import "./variables.less";
@import "./mixins.less";

.card {
  padding: @space-md;
  border: 1px solid fade(@color-brand, 20%);
  .title {
    color: @color-brand; // 编译成 .card .title
    font-size: 14px + 2px; // 运算
  }
  .actions {
    .flex-center(12px);
  }
}
```

编译结果（示意）：`.card .title { color: #2563eb; font-size: 16px; }`，mixin 展开成真实声明。

**遇见问题 → 怎么办**

| 现象 | 处理 |
| --- | --- |
| 浏览器里样式全无 | 确认构建配了 `less` 加载器；看 Network 是否只有未编译的 `.less` |
| 改了 `@color` 页面不变 | 清缓存 / 重启 dev；检查是否 import 了另一份同名变量文件 |
| 嵌套选择器权重爆炸 | 限制嵌套 ≤3 层；组件用 BEM / scoped，少写 `.a .b .c .d` |

### 3. Less 和 Sass / 原生 CSS 变量怎么选？（对应第 3 问）

| 维度 | Less | Sass | CSS `var(--x)` |
| --- | --- | --- | --- |
| 语法 | 很像 CSS，`@var` | 更强（模块、条件等） | 原生 |
| 生效时机 | **编译期**替换 | 编译期 | **运行时**可改 |
| 主题切换 | 要重新编译或另出 CSS 变量桥 | 同左 | `[data-theme]` 即时切 |
| 选型 | 团队已有 Less / 老项目 | 大型样式工程常见 | 新主题、暗色模式优先 |

**业务例子**：管控台把品牌色放 `variables.less`；若要做暗色运行时切换，Less token 再映射到 `--color-brand`，运行时只改 CSS 变量。

## 可能追问

- 嵌套太深有什么问题？→ 选择器过重、难覆盖、体积涨，调试痛苦。
- Less 变量和 `var(--x)` 能混用吗？→ 能：Less 负责编译期默认值，关键主题色导出成 CSS 变量。
- 如何按需？→ 按路由/组件拆 less，避免一个几千行的 `global.less`。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
