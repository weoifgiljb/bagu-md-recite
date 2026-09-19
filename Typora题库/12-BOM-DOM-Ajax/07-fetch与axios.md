# 题 7：fetch 和 axios 怎么比？你会封装吗？

## 面试官可能怎么问

- fetch 有哪些坑？
- 怎么取消请求？
- 拦截器做什么？

## 口述结构（90 秒）

1. fetch 是原生；axios 是完整客户端体验
2. fetch 最大坑：HTTP 错误不自动进 catch
3. 取消：AbortController；超时自己包一层
4. 封装：实例 + 请求/响应拦截器 + 统一错误

## 参考答案

### 1. fetch 有哪些坑（对照表）

| 点 | fetch | axios |
| --- | --- | --- |
| HTTP 4xx/5xx | 默认 **resolve**，要自己看 `ok` | 进 reject（可配） |
| 超时 | 无内置 | `timeout` 配置 |
| 拦截器 | 自己包函数 | 原生支持 |
| JSON | 手动 `res.json()` | 常自动变换 |
| 上传进度 | 不直观 | 较方便（或 XHR） |
| Node/浏览器 | 现代都可 | 双端成熟 |

```js
const res = await fetch('/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify(body),
  signal,
})
if (!res.ok) {
  const errText = await res.text()
  throw new Error(`HTTP ${res.status}: ${errText}`)
}
return res.json()
```

### 2. 怎么取消请求（标准步骤）

1. 创建 `const ac = new AbortController()`  
2. 请求传入 `{ signal: ac.signal }`（fetch/axios 均可）  
3. 超时：`setTimeout(() => ac.abort(), 15000)`  
4. 路由离开、重复搜索、切换会话：立刻 `ac.abort()`  
5. catch 里识别 `AbortError`，不要当致命故障弹窗  

流式对话切换会话时必须 abort，否则旧流继续 `append` 会**串台**。

### 3. 拦截器做什么（封装清单）

请求拦截：加 `Authorization`、幂等键、语言头、开始打点。  
响应拦截：解包 `{ code, data }`、`401` 清登录态并跳转、`429` 退避重试、统一 Toast。

```js
const http = axios.create({ baseURL: '/api', timeout: 15000 })
http.interceptors.request.use((cfg) => {
  const token = localStorage.getItem('token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})
http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    if (err.response?.status === 401) redirectLogin()
    return Promise.reject(err)
  },
)
```

选型：JSON CRUD 用 axios 实例；SSE/流式用 fetch + ReadableStream。



### 5. 封装时的最小清单（面试收口）

1. 一个 `createHttp()` 实例，禁止满项目裸 fetch 各写各的头  
2. 请求侧：token、语言、`X-Request-Id`  
3. 响应侧：业务 code 与 HTTP status 分层处理  
4. 可取消：每个页面级请求绑定 signal  
5. 流式与 JSON 分流：两套 client，错误模型尽量统一  

这样讲完，面试官能感到你不是背 API 对比，而是做过工程封装。

## 可能追问

- 为什么不用 EventSource？→ 难自定义 Header。  
- 如何防重复提交？→ 按钮锁 + 取消上一次 + 幂等键。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
