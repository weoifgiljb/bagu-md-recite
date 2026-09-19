# 题 7：vue-router 导航守卫和懒加载怎么讲？

## 面试官可能怎么问

- 全局/路由独享/组件内守卫区别？
- 怎么做登录拦截？
- 路由懒加载怎么写、有什么好处？

## 口述结构（90 秒）

1. 守卫：beforeEach → beforeEnter → 组件守卫 → afterEach
2. 登录：beforeEach 校验 token + 白名单 + roles
3. 懒加载：`() => import()` 拆 chunk
4. history 模式要服务器回退；标题埋点放 afterEach

## 参考答案

**对应问 1：三种守卫**
- **全局** `router.beforeEach`：登录态、权限、埋点前置
- **路由独享** `beforeEnter`：某个活动页是否下线、是否灰度
- **组件内** `onBeforeRouteLeave`：未保存提示；`onBeforeRouteUpdate`：同一组件 params 变化重新拉数（如 `/user/:id`）

完整链路（简化口述）：确认导航 → 全局前置 → 路由 beforeEnter → 复用组件 update / 非复用 leave+enter → 解析异步组件 → 全局 afterEach。

**对应问 2：登录拦截落地**
```ts
router.beforeEach(async (to) => {
  if (to.meta.public) return true
  const user = useUserStore()
  if (!user.token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (!user.profile) await user.fetchProfile()
  if (to.meta.roles && !user.hasRole(to.meta.roles)) {
    return { name: '403' }
  }
  return true
})
```
注意：先 `app.use(pinia)` 再解析路由；401 时清 token 避免死循环。

**对应问 3：懒加载**
```ts
{
  path: '/chat/:id?',
  name: 'chat',
  component: () => import('@/views/Chat.vue'),
  meta: { roles: ['user'] }
}
```
好处：首包更小、按路由加载。可配加载中组件。Webpack/Vite 会打出单独 chunk。

**业务例子**
管理端 `meta.roles=['admin']`；C 端聊天页懒加载；登录后 `redirect` 回原页。

## 可能追问

- hash vs history？→ history 需 Nginx `try_files ... /index.html`。
- 重复导航报错？→ 捕获 Promise 或升级 vue-router4 行为。
- 传参？→ params/query；强制刷新子组件可用 `:key="$route.fullPath"`。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
