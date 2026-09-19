# 题 1：ref 和 reactive 有什么区别？什么时候用哪个？

## 面试官可能怎么问

- ref 和 reactive 区别？
- 为什么 ref 要 `.value`，模板里却不用？
- reactive 解构会丢响应式吗？怎么解决？

## 口述结构（90 秒）

1. ref 可包任意类型；reactive 只适合对象
2. 脚本里 ref 要 `.value`，模板自动解包
3. reactive 解构/整对象替换会丢代理；用 `toRefs` 或改用 ref
4. 基础类型/常整体替换 → ref；结构稳定的对象也可用 reactive，团队统一即可

## 参考答案

**对应问 1：区别**
- `ref(x)`：把值放进带 `.value` 的盒子，number/string/object 都行。
- `reactive(obj)`：对对象做深度 Proxy，没有 `.value`。
- 访问：脚本 `count.value++`；模板里写 `count` 即可（编译期解包）。

**对应问 2：为何模板不用 .value**
模板编译会识别顶层 ref 并自动解包。脚本是普通 JS，必须 `.value`，否则改的是盒子本身引用。

**对应问 3：解构丢失**
```ts
const state = reactive({ a: 1, b: 2 })
const { a } = state // a 是普通 number，不再响应
const { a: ar, b: br } = toRefs(state) // ar.value 仍响应
```
整对象替换也不行：`state = reactive({...})` 之后又 `state = { a: 3 }` 会丢掉代理。应改属性或外层用 `ref`。

**选型建议**
- 原始值、可能整体换掉的对象（列表常 `ref([])`）→ ref  
- 表单模型字段多、结构稳定 → reactive 或 `ref({...})` 皆可，项目统一一种

**业务例子**
对话 `messages = ref([])`；筛选条件 `filters = reactive({ q:'', tag:'' })` 或统一 ref。

## 可能追问

- shallowRef？→ 只代理 `.value` 这一层，大数组/第三方实例避免深代理。
- toRef / toRefs？→ 单个字段 vs 批量。
- 为何弃 defineProperty？→ Proxy 能听增删与数组下标。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
