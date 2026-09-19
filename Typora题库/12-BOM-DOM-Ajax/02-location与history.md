# 题 2：location 和 history 怎么用？和前端路由关系？

## 面试官可能怎么问

- location 有哪些字段？
- history.pushState 干什么？
- hash 路由和 history 路由区别？

## 口述结构（90 秒）

1. location 拆解 URL 各段并支持跳转
2. pushState 改 URL、压栈，但不自动渲染
3. 前端路由 = 听 URL 变化 + 匹配组件
4. history 模式必须服务端回退，否则刷新 404

## 参考答案

### 1. location 有哪些字段（逐项会用）

常用字段：`href`（完整）、`origin`、`protocol`、`host`、`pathname`、`search`（含 `?`）、`hash`（含 `#`）。

```js
// 读查询参数
const q = new URLSearchParams(location.search)
const tab = q.get('tab') || 'all'

// 跳转策略
location.assign('/reports')   // 历史可回
location.replace('/login')    // 不把登录页留在后退栈
location.reload()
```

步骤（筛选进 URL）：  
1. 用户改筛选 → 组装新 query  
2. `history.replaceState` 或 `router.replace({ query })`  
3. 刷新后从 `location.search` 恢复，避免「一刷新筛选丢了」

### 2. history.pushState 干什么

作用：**在不向服务器要整页 HTML 的前提下**，改变地址栏并写入历史栈。

```js
history.pushState({ conversationId: 'c1' }, '', '/chat/c1')
history.replaceState({ conversationId: 'c1' }, '', '/chat/c1') // 不新增多余条目

window.addEventListener('popstate', (e) => {
  // 后退/前进到达该条目；根据 location 或 e.state 渲染
  loadConversation(location.pathname)
})
```

步骤对接 SPA：  
1. 点击菜单 → 路由 `push` → 内部 `pushState`  
2. 匹配路由表 → 挂载组件  
3. 用户后退 → `popstate` → 再匹配一次  

没有第 2/3 步，光 `pushState` 只会「地址变了，页面还是旧的」。

### 3. hash 路由和 history 路由区别

| 维度 | hash：`/#/chat` | history：`/chat` |
| --- | --- | --- |
| 依赖 | `location.hash` + `hashchange` | `pathname` + `pushState`/`popstate` |
| 刷新 | hash 一般不进服务器路径，少 404 | 服务器必须把未知路径回退到 `index.html` |
| 观感/SEO | 带 `#`，偏旧 | URL 干净，更常见于现网 |
| Vue Router | `createWebHashHistory()` | `createWebHistory()` |

生产 history 模式 Nginx 示意：`try_files $uri $uri/ /index.html;`

### 4. 业务例子

对话页把 `conversationId` 放进路径或 query；OAuth 回调成功后用 `replace` 清掉 `code`，防止刷新重复绑定。

## 可能追问

- pushState 的 title 参数？→ 多数浏览器忽略。  
- 能否 push 到别的域名？→ 不能，受同源限制。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
