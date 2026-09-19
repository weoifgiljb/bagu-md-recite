# 题 2：computed 和 watch 有什么区别？怎么选？

## 面试官可能怎么问

- computed 和 watch 分别适合什么场景？
- computed 为什么能缓存？和 methods 差在哪？
- watch 的 deep / immediate / flush 怎么用？watchEffect 呢？

## 口述结构（90 秒）

1. 一句话：computed 是「派生值」，watch 是「副作用响应变化」
2. computed 依赖收集 + 缓存，模板多次读只算一次；methods 每次调用都算
3. watch 显式指定源，可拿 old/new；watchEffect 自动收集依赖，立即跑
4. 选型：能算出值用 computed；要请求/改 DOM/同步外系统用 watch
5. 收尾：deep 贵、immediate 补首跑、flush 控时序

## 参考答案

### 1. 场景怎么选？

| 需求 | 用谁 |
| --- | --- |
| 由已有状态算出展示用值（全名、过滤列表、总价） | `computed` |
| 状态变了要发请求、写 localStorage、调第三方 SDK | `watch` / `watchEffect` |
| 模板里简单表达式且只用一次 | 模板内联即可，不必硬上 computed |

原则：**能声明成值就别写成副作用**。面试常踩的坑是用 `watch` 去「算出另一个 ref」再给模板用——应改成 `computed`。

### 2. computed 缓存 vs methods

```ts
const list = ref([{ price: 10 }, { price: 20 }])
const total = computed(() => list.value.reduce((s, i) => s + i.price, 0))

// methods：每次渲染/每次调用都重新算
function getTotal() {
  return list.value.reduce((s, i) => s + i.price, 0)
}
```

- `computed`：依赖（`list`）不变时，多次访问 `total.value` **复用缓存**；依赖变了才脏检查重算。
- `methods`：无缓存，适合「带参数的动作」或「每次必须最新且开销很小」的计算。
- 赋值：`computed` 默认只读；需要双向时用 `{ get, set }`（如配合 `v-model` 拆 props）。

```ts
const fullName = computed({
  get: () => first.value + ' ' + last.value,
  set: (v: string) => {
    const [a, b = ''] = v.split(' ')
    first.value = a
    last.value = b
  },
})
```

### 3. watch / deep / immediate / flush / watchEffect

```ts
// 显式源 + old/new（适合对比前后）
watch(
  () => props.userId,
  async (id, prev) => {
    if (!id || id === prev) return
    data.value = await fetchUser(id)
  },
  { immediate: true }, // 首屏也要拉一次
)

// 对象内部字段变也要听：deep（大对象慎用）
watch(
  form,
  () => { /* 校验/草稿保存 */ },
  { deep: true, flush: 'post' }, // DOM 更新后再跑，适合量尺寸
)

// 自动收集依赖，创建时立刻执行
watchEffect((onCleanup) => {
  const ctrl = new AbortController()
  onCleanup(() => ctrl.abort())
  load(keyword.value, ctrl.signal)
})
```

要点：

1. **deep**：对对象/数组内部变更敏感，但遍历开销大；能听具体字段就写 `() => obj.a.b`。
2. **immediate**：补「首次也要执行」；常和路由参数、props 拉数一起用。
3. **flush**：`'pre'`（默认，组件更新前）、`'post'`（更新后，读 DOM）、`'sync'`（极少用，同步触发）。
4. **watchEffect**：写法短，但拿不到 oldValue；清理副作用用 `onCleanup`。
5. 停止：返回的 `stop()`，或组件卸载时自动停（setup 里创建的）。

**业务例子**：聊天会话切换用 `watch(() => route.params.id, ...)` 拉历史；未读数角标用 `computed` 从 messages 过滤；输入防抖搜索用 `watchEffect` + `onCleanup` 取消上一次请求。

**验收**：同一 computed 在模板出现两处，依赖不变时不应重复重算（可打 log 验证）；切路由取消未完成请求，避免串数据。

## 可能追问

- computed 里能改别的状态吗？→ 不要；应保持纯函数，副作用放 watch。
- 监听多个源？→ `watch([a, b], ([na, nb], [oa, ob]) => {})`。
- `watch` 数组默认浅听 push？→ 替换数组能触发；改下标元素要 deep 或听具体项。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
