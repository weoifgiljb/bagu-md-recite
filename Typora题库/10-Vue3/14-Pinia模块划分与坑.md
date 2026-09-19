# 题 14：Pinia 多 store 怎么拆？有哪些坑？

## 面试官可能怎么问

- 一个大 store 还是多个？
- setup store 和 option store？
- store 之间能互相调用吗？

## 口述结构（90 秒）

1. 按领域拆：user / chat / permission，拒绝上帝 store
2. UI 临时态留在组件；跨页业务态进 Pinia
3. setup / option 都能用，团队统一即可
4. 可互调，但要防环依赖与初始化时序

## 参考答案

### 1. 一个大 store 还是多个？

**多个按领域。** 标准：

| 放 Pinia | 放组件 ref |
| --- | --- |
| 登录用户、权限、当前企业 | 弹窗开关、输入框草稿 |
| 跨页会话 id、主题 | 一次性 loading 微调 |
| 要持久化/调试的业务态 | 纯展示派生且用完即弃 |

步骤划界：问「刷新后还要吗？别的页要用吗？」——两问皆否就别进 Pinia。

### 2. setup store vs option store

```ts
// option
defineStore('chat', {
  state: () => ({ messages: [] as Msg[] }),
  getters: { count: (s) => s.messages.length },
  actions: { async load() { /* ... */ } },
})

// setup（Composition 风格，灵活）
defineStore('chat', () => {
  const messages = ref<Msg[]>([])
  const count = computed(() => messages.value.length)
  async function load() { /* ... */ }
  return { messages, count, load }
})
```

选型：新代码可 setup；与旧 option 混用时，**调用方式都是 `useXxxStore()`**，别纠结宗教战争。

### 3. store 互调与坑

```ts
const user = useUserStore()
const perm = usePermissionStore()
// 在 action 里：
async function enterApp() {
  await user.fetchMe()
  await perm.loadByRoles(user.roles)
}
```

坑清单：  
1. **环依赖**：A import B、B import A → 初始化 undefined；用延迟 `useStore()` 放进函数内  
2. **把整表数据塞满 Pinia** → 内存膨胀；分页数据放页内或 query cache  
3. **在 store 里直接操作 DOM/router** 过深 → 难测；通过返回值/事件让页面跳  
4. **解构丢响应式**：`const { token } = store` 要 `storeToRefs(store)`  

业务例子：`user` + `permission` + `chat` 三店；聊天消息按会话缓存上限淘汰。


### 4. 推荐目录与协作约定

```text
stores/
  user.ts
  permission.ts
  chat.ts
  app.ts          // 主题、语言、全局 toast 开关
```

约定：  
1. 跨 store 编排放在「用例函数」或页面，而不是互相偷偷改私有 state  
2. 异步请求进 actions，派生进 getters/computed  
3. 持久化白名单写在 store 旁注释，CR 时好查  
4. 单测优先测 actions 的状态迁移，少测框架本身  

这样拆完，面试官能听出你有模块边界，而不是「一个 useMainStore 一万行」。

## 可能追问

- 和 Vuex 差在？→ 无 mutations 强制、TS 友好、模块天然拆。  
- 要不要规范层？→ 超大项目可加 service 层，store 只编排。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
