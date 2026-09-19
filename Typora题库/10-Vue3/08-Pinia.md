# 题 8：Pinia 相比 Vuex 有什么好处？怎么组织 store？

## 面试官可能怎么问

- 为什么 Vue3 推 Pinia？
- option store 和 setup store？
- 持久化怎么做？

## 口述结构（90 秒）

1. 无 mutation、TS 友好、多 store 自然拆分
2. option / setup 两种写法，团队统一
3. 按领域拆：user / chat / permission
4. 持久化只存必要字段；局部 UI 别进 store

## 参考答案

**对应问 1：为什么 Pinia**
- 去掉 mutation，action 里直接改 state，心智负担小
- 完美配合 `<script setup>` 与类型推断
- 多个 `defineStore` 即可，不必嵌套 modules
- DevTools、热更新体验好；体积更小

**对应问 2：两种写法**
```ts
// setup store（推荐复杂逻辑）
export const useChatStore = defineStore('chat', () => {
  const conversationId = ref('')
  const messages = ref<Msg[]>([])
  async function load(id: string) {
    conversationId.value = id
    messages.value = await api.list(id)
  }
  return { conversationId, messages, load }
})
```
option store 用 `state/getters/actions`，简单 CRUD 也够用。`$reset` 在 option 更现成；setup 需手写初始快照。

**对应问 3：持久化**
- 插件 `pinia-plugin-persistedstate`，或 `store.$subscribe` 写 `localStorage`
- **白名单字段**：token、主题、草稿；不要把全部消息列表塞进去
- 启动时 hydrate；加 `version` 做迁移/清理

**组织与边界**
- 跨页、要调试、要持久 → Pinia
- 弹窗开关、输入框临时值 → 组件 ref
- 树内上下文（当前表单总线）→ provide/inject

**业务例子**
`useUserStore` 管身份与权限码；`useChatStore` 管会话与流式缓冲；路由守卫读 userStore。

## 可能追问

- store 互相调用？→ 可以，注意环依赖。
- 在路由守卫用 store？→ pinia 安装后再用。
- 替代 Vuex 路径？→ 新项目直接 Pinia；旧项目可渐进替换。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
