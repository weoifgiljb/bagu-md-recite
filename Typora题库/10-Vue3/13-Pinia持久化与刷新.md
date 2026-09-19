# 题 13：Pinia 如何做持久化？刷新后状态怎么恢复？

## 面试官可能怎么问

- 刷新页面 Pinia 状态会丢吗？
- 用 localStorage 还是 sessionStorage？
- 和登录态怎么配合？

## 口述结构（90 秒）

1. 默认内存态，刷新必丢
2. 持久化：插件或 `$subscribe`/`watch` 写 Storage
3. 只存必要字段；大列表重启拉接口
4. 启动 hydrate；做版本号/过期清理

## 参考答案

### 1. 刷新会丢吗？

会。Pinia store 默认在内存；F5 后重新创建应用，状态回到 initial。  
要跨刷新：自己持久化，或 `pinia-plugin-persistedstate`。

### 2. 手写最小实现（步骤）

```ts
// stores/user.ts
export const useUserStore = defineStore('user', {
  state: () => ({ token: '', profile: null as null | Profile }),
  actions: {
    hydrate() {
      const raw = localStorage.getItem('user-v1')
      if (!raw) return
      try {
        const data = JSON.parse(raw)
        if (data.v !== 1) return localStorage.removeItem('user-v1')
        this.token = data.token || ''
        this.profile = data.profile || null
      } catch { localStorage.removeItem('user-v1') }
    },
    logout() {
      this.$reset()
      localStorage.removeItem('user-v1')
    },
  },
})

// main.ts
const user = useUserStore(pinia)
user.hydrate()
user.$subscribe((_m, state) => {
  localStorage.setItem('user-v1', JSON.stringify({
    v: 1,
    token: state.token,
    profile: state.profile,
  }))
})
```

插件写法（示意）：`persist: { paths: ['token'] }`——**只白名单字段**。

### 3. localStorage vs sessionStorage

| 场景 | 选型 |
| --- | --- |
| 记住登录、主题、语言 | `localStorage` |
| 关 Tab 即废的敏感草稿 | `sessionStorage` |
| 巨型消息列表/报表行 | **别持久化**，只存 id，进页再请求 |

### 4. 和登录态配合

1. 启动：`hydrate` → 有 token 再拉 `/me` 校验  
2. `401`：清 store + 清 Storage + 跳登录  
3. 多 Tab：听 `storage` 事件同步登出  
4. SSR：Storage 仅浏览器；服务端不要读  

业务例子：聊天草稿可 local；消息数组只存 `conversationId`。


### 5. 验收口径

1. 刷新后 token 仍在，且 `/me` 能成功  
2. 登出后 Storage 对应 key 消失，另一 Tab 同步退出  
3. 只持久化白名单字段，Application 面板看不到巨型 messages  
4. 改了持久化结构会升 `v` 并清理旧 key，避免脏数据 hydrate 报错  

把这四条讲完，比只说「用了某某插件」更像做过登入态工程。

插件选型一句：小项目手写 `$subscribe` 足够；字段多、要路径白名单再用 `pinia-plugin-persistedstate`。

## 可能追问

- 加密 Storage？→ 前端加密防不了 XSS 读明文密钥；根本仍是少放敏感、HttpOnly 优先。  
- 配额满了？→ catch QuotaExceeded，降级只存 token。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
