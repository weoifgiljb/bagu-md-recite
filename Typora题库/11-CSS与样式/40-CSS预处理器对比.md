# 题 40：Less / Sass / Stylus 怎么对比？现在还需要吗？

## 面试官可能怎么问

- 三者差别？
- 和 CSS 原生能力重复吗？
- 你项目为什么用 Less？

## 口述结构（90 秒）

1. 三者都是**预处理器**：变量、嵌套、mixin/函数、模块导入，编译成普通 CSS
2. **差别**：Sass（Dart Sass）生态与能力最强；Less 语法贴近 CSS、中后台/Ant Design 体系常见；Stylus 灵活但团队少
3. **和原生重复**：原生已有 CSS 变量、嵌套（渐进）、`@import`/`@layer` 等；预处理仍擅长复杂 mixin、设计 token 编译、存量主题
4. 选型诚实讲：跟团队与 UI 库；新项目可「CSS 变量 + 适度嵌套 / 原子化」，动态换肤优先 CSS 变量

## 参考答案

### 1. 三者差别（回答该问）

| 维度 | Sass/SCSS | Less | Stylus |
| --- | --- | --- | --- |
| 语法 | SCSS 最像 CSS；缩进语法另有一套 | 很像 CSS，学习成本低 | 可省略括号/分号，更自由 |
| 生态 | 最大；文档、工具链成熟 | 中大型中后台多 | 相对小众 |
| 能力 | 模块、混合、函数、列表/map 很强 | 变量、mixin、嵌套够用 | 表达力强但可读性看团队 |
| 实现 | 用 **Dart Sass**（`node-sass` 已弃） | less 包 / less-loader | stylus |
| 典型场景 | 设计系统、复杂样式工程 | Ant Design、很多 Vue 中后台 | 老项目或偏好极简语法 |

```scss
// SCSS
$brand: #1677ff;
.btn {
  background: $brand;
  &:hover { filter: brightness(0.95); }
}
```

```less
// Less
@brand: #1677ff;
.btn {
  background: @brand;
  &:hover { filter: brightness(0.95); }
}
```

### 2. 和 CSS 原生能力重复吗？（回答该问）

部分重复，但职责仍可拆：

| 能力 | 原生 CSS | 预处理器仍有价值 |
| --- | --- | --- |
| 变量 | `var(--x)` 运行时可切换 | 编译期常量、色板运算、多份主题文件生成 |
| 嵌套 | 现代浏览器已支持（注意特异性与转译） | 旧浏览器转译、统一团队风格 |
| 复用 | `@layer`、自定义属性、工具类 | mixin、函数、循环生成间距/色阶 |
| 模块 | 原生 import 仍在演进 | 成熟的文件拆分与构建集成 |

结论：**不是「有了原生就立刻删 Less」**，而是新功能优先原生变量做运行时，预处理收敛到 token 与存量。

### 3. 项目为什么用 Less？（回答该问——按真实情况改口）

可参考的诚实答法（结合业务）：

1. **UI 库约束**：Ant Design / 部分组件库主题基于 Less 变量，改品牌色走官方 less 变量覆盖成本最低。  
2. **存量一致**：仓库已是 `.less`，构建（vite/`less-loader`）现成，团队都熟。  
3. **分工**：Less 管组件结构嵌套与编译期 token；**运行时亮暗切换**用 CSS 变量（见题 36），避免为换肤打多份 CSS 包。  
4. 若从零新项目且无 Less 依赖：可 SCSS 或「纯 CSS + PostCSS + 原子化」，不必为了简历强上预处理器。

```less
// 编译期灌默认，运行时用 CSS 变量覆盖
@primary: #1677ff;
:root {
  --primary: @primary;
}
.btn { background: var(--primary); }
```

## 可能追问

- Dart Sass vs node-sass？→ 用 Dart Sass；node-sass 绑定旧 Node、已不维护。
- 和 Tailwind？→ 原子类提速搭建；设计系统仍要 token（可用 CSS 变量）。二者可并存。
- Stylus 还值得学吗？→ 了解即可，新项目优先 Sass/Less/原生。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
