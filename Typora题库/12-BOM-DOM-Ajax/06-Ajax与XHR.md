# 题 6：Ajax 是什么？XHR 关键状态说一下？

## 面试官可能怎么问

- Ajax 原理？
- readyState 各是什么？
- 同步请求为什么别用？

## 口述结构（90 秒）

1. Ajax：用 JS 发请求，局部更新，不整页刷新
2. 老 API 是 XMLHttpRequest；新项目多用 fetch/axios
3. readyState 是客户端状态机，status 是 HTTP 码
4. 同步 XHR 会冻住主线程，线上禁止

## 参考答案

### 1. Ajax 原理（步骤版）

1. 用户触发（点搜索、切页、发送消息）  
2. JS 创建 XHR/fetch，组装 URL/方法/头/体  
3. 浏览器发 HTTP；当前文档不卸载  
4. 响应返回后，JS 更新状态/DOM（表格行、气泡内容）  
5. 失败则走错误态与重试策略  

```js
const xhr = new XMLHttpRequest()
xhr.open('GET', '/api/list?page=1')
xhr.setRequestHeader('Accept', 'application/json')
xhr.onload = () => {
  if (xhr.status >= 200 && xhr.status < 300) {
    const data = JSON.parse(xhr.responseText)
    renderList(data)
  } else {
    showError(`业务/HTTP 错误 ${xhr.status}`)
  }
}
xhr.onerror = () => showError('网络失败')
xhr.send()
```

### 2. readyState 各是什么

| readyState | 名称 | 含义 |
| --- | --- | --- |
| 0 | UNSENT | 已创建，未 `open` |
| 1 | OPENED | 已 `open`，可设头，可 `send` |
| 2 | HEADERS_RECEIVED | 响应头可用 |
| 3 | LOADING | 响应体下载中（可多次触发） |
| 4 | DONE | 结束（成功或失败都可能到 4） |

开口一定补一句：**到了 4 还要看 `status`**。`200` 成功、`401` 未登录、`500` 服务器错，和 readyState 不是一回事。

上传进度（面试加分）：

```js
xhr.upload.onprogress = (e) => {
  if (e.lengthComputable) setProgress(e.loaded / e.total)
}
```

### 3. 同步请求为什么别用

`xhr.open(method, url, false)` 会让 `send()` **阻塞主线程**：页面点不动、动画停、输入框卡死。  
替代步骤：全部异步；需要顺序就用 `async/await` 或 Promise 链；并发用 `Promise.all`（注意限流）。

### 4. 业务例子

附件上传要进度条时仍常见 XHR；普通 JSON 接口用 axios。聊架构时强调：**取消、超时、鉴权头** 比纠结 API 名字更重要。

## 可能追问

- withCredentials？→ 跨域是否带 cookie。  
- onload 和 onreadystatechange？→ 前者更简洁；后者可观察中间态。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
