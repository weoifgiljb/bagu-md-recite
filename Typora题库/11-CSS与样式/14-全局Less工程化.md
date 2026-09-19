# 题 14：项目里「全局 Less」一般怎么组织？有什么坑？

## 面试官可能怎么问

- 全局变量怎么注入每个组件？
- 和 Vue scoped 一起用注意什么？
- 如何避免样式污染？

## 口述结构（90 秒）

1. 分层：`variables` / `mixins` / `reset` / 极少 `global`
2. 构建 `additionalData`（或等同配置）自动注入变量，避免每个 SFC 手写 `@import`
3. 全局只放 reset + token；业务类名用 BEM / scoped，防污染
4. 改全局先评估影响面；覆盖用 `:deep` 或更高特异性，主题用 CSS 变量桥

## 参考答案

### 1. 全局变量怎么注入每个组件？（对应第 1 问）

**推荐目录**
```
styles/
  variables.less   // 色板、字号、间距
  mixins.less
  reset.less
  global.less      // 极少工具类，能不写就不写
```

**Vite + Vue 示例（自动注入，组件里直接用 `@color-brand`）**
```ts
// vite.config.ts
export default defineConfig({
  css: {
    preprocessorOptions: {
      less: {
        additionalData: `@import "@/styles/variables.less";\n@import "@/styles/mixins.less";\n`,
        javascriptEnabled: true, // 若用到老 less 插件再开
      },
    },
  },
});
```

**遇见问题 → 怎么办**
1. 报 `variable @xxx is undefined`：检查 `additionalData` 路径别名是否解析；改成相对路径试一次。
2. 每个文件都写 `@import` 又重复又易漏：统一放到 `additionalData`，业务文件禁止再手写一份。
3. 注入了 `reset.less` 导致组件样式被洗：`additionalData` **只注入 variables/mixins**，reset 只在入口 `main.ts` import 一次。

### 2. 和 Vue scoped 一起用注意什么？（对应第 2 问）

- SFC 里 `<style lang="less" scoped>`：Less 先编译，再由 Vue 给选择器加 `data-v-xxxx`。
- **改子组件根节点样式**：用 `:deep(.child-class)`（Vue3），不要指望父 scoped 直接打到子内部。
- **改子组件内部深层**：同样 `:deep`；能改子组件自己的样式就别在父里穿透。
- **第三方组件**：优先走组件提供的 props/`popper-class`；必须覆盖时用单独 `unscoped` 文件并加命名空间前缀，如 `.app-modal .el-dialog__body`。

```vue
<style lang="less" scoped>
.card {
  :deep(.ant-btn) { border-radius: 8px; }
}
</style>
```

### 3. 如何避免样式污染？（对应第 3 问）

| 做法 | 说明 |
| --- | --- |
| 全局极简 | 全局只 reset + token，禁止 `.button { }` 这种通用类 |
| 命名空间 | 业务前缀 `.edu-` / BEM；工具类用明确前缀 |
| scoped | 组件默认 scoped |
| 审查入口 | Code review 盯 `styles/global.less` 的新增 |
| 主题出口 | 运行时换肤用 CSS 变量，少改全局 Less 实值 |

**业务例子**：教育管控台品牌色走 Less token；暗色用 `[data-theme="dark"] { --color-bg: ... }`，Less 编译出默认值，运行时只切变量。

## 可能追问

- Less 修改是否热更新？→ 开发态依赖 HMR；生产要重新构建产物。
- 和 Tailwind 混用？→ 可以，但 **颜色源只能有一个**（token 对齐），避免两套色板。
- `additionalData` 导致每个模块都重复一大段 CSS？→ 只注入变量/mixin（编译期），不要注入会产出真实选择器的 reset。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
