# 题 12：Vue3 相对 Vue2 面试要讲哪些变化？

## 面试官可能怎么问

- Vue3 新特性有哪些？
- 为什么要迁移？
- Composition API 解决什么痛点？

## 口述结构（90 秒）

1. 响应式换 Proxy；能听增删属性
2. Composition API / script setup，逻辑按功能聚合
3. 编译期优化 + tree-shaking，性能与体积更好
4. Fragment、Teleport、Suspense；生态转向 Pinia

## 参考答案

**对应问 1：新特性（挑重点讲）**
- Composition API、`<script setup>`
- Proxy 响应式（替代 Object.defineProperty）
- 多根节点（Fragment）
- `Teleport`：弹层挂到 body
- 生命周期更名：`beforeDestroy` → `beforeUnmount`
- 新内置：Suspense（异步边界，评估后再上生产）

**对应问 2：迁移动机**
- Vue2 已结束维护，安全与生态在 Vue3
- TS 体验质变，大型项目可维护性更好
- 包体积、更新性能通常优于 Vue2
- 新库（Pinia、Vite 模板）默认 Vue3

**对应问 3：Composition 解决的痛**
Options API 下，同一个「流式对话」的 data/methods/watch 散落；mixin 易命名冲突、来源不清。  
Composition 可写成 `useChatStream()`，在列表页和弹窗复用，依赖关系清晰，也更好单测。

**业务例子**
弹层用 Teleport 摆脱父级 `overflow:hidden`；把 SSE 重连逻辑收成 composable；状态用 Pinia 替代 Vuex。

## 可能追问

- Options 还能用吗？→ 能，可混用；新代码建议 setup。  
- 过滤器？→ 已移除，改方法/computed。  
- Vue2 项目怎么迁？→ 先上兼容构建 / 分模块渐进。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
