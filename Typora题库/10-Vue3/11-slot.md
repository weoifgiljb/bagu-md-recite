# 题 11：Vue slot 有哪几种？作用域插槽怎么用？

## 面试官可能怎么问

- 默认插槽、具名插槽、作用域插槽区别？
- 和 props 传渲染函数比有什么好处？
- 典型业务怎么用？

## 口述结构（90 秒）

1. 插槽是父传给子的结构坑位
2. 具名：多个坑；默认叫 default
3. 作用域插槽：子把数据回传给父渲染
4. 表格列、卡片操作区最常见

## 参考答案

**对应问 1：三种**
```vue
<!-- 子组件 Panel.vue -->
<template>
  <header><slot name="title">默认标题</slot></header>
  <main><slot /><!-- 默认插槽 --></main>
  <div class="row" v-for="row in rows" :key="row.id">
    <slot name="cell" :row="row" :index="index" />
  </div>
</template>
```
父：
```vue
<Panel>
  <template #title>审评证据</template>
  <p>正文</p>
  <template #cell="{ row }">{{ row.name }}</template>
</Panel>
```

**对应问 2：好处**
- 布局封装在子组件，父只填内容，API 比「传 VNode/render 函数」更友好
- 作用域插槽让子控制数据遍历，父控制单元格长相（表格列定制）
- 设计稿变更时少改子组件内部

**对应问 3：业务**
- 布局壳：header/footer 具名插槽
- 通用 Table：`#cell="{ row, column }"`
- Evidence 卡片：默认插槽放摘要，`#actions` 放按钮

## 可能追问

- 动态槽名？→ `#[name]`。  
- 条件槽？→ `v-if="$slots.footer"`。  
- 和 props 同时用？→ 数据 props，结构 slots。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
