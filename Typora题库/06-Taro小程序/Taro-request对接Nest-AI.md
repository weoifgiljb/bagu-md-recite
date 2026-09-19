# 题 2：Taro.request 怎么封装？统一 envelope 错误怎么处理？

## 面试官可能怎么问

- Taro.request / wx.request 和 axios 差在哪？
- 统一响应 envelope（code/data/message）怎么解析？
- AI 接口超时、401、429 怎么映射到 UI？

## 口述结构（90 秒）

1. 封装一层 client：基址、header、timeout、错误归一
2. 先看 HTTP status，再看业务 code；取出 data
3. 网络/超时/鉴权/限流/业务失败 → 统一错误类型 + 可读文案
4. AI 生成类单独加大 timeout；UI 给重试，不只 console

## 参考答案

### 1. 和浏览器 axios 的差异

小程序端常见 `Taro.request` 或直接 `wx.request`：  
- 必须 **HTTPS + 合法域名**（后台配置）；不是浏览器 CORS 语义。  
- 无完整 Cookie 自动策略时，Token 多放 Header；上传用 `uploadFile`。  
- 返回形态是 `{ statusCode, data, header }`，**不会**像 axios 默认抛非 2xx（取决于你是否封装）。

```ts
// 统一 client 骨架
export function request<T>(opt: {
  url: string; method?: 'GET'|'POST'; data?: unknown
  header?: Record<string,string>; timeoutMs?: number
}): Promise<T> {
  const timeoutMs = opt.timeoutMs ?? 8000
  return new Promise((resolve, reject) => {
    Taro.request({
      url: join(BASE_URL, opt.url),
      method: opt.method || 'GET',
      data: opt.data,
      timeout: timeoutMs,
      header: { 'Content-Type': 'application/json', ...authHeader(), ...opt.header },
      success: (res) => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          reject({ type: 'http', statusCode: res.statusCode, body: res.data })
          return
        }
        resolve(unwrapEnvelope<T>(res.data))
      },
      fail: (err) => reject({ type: 'network', errMsg: err.errMsg })
    })
  })
}
```

### 2. envelope 解析步骤

后端常见：`{ code: 0, data: {...}, message: 'ok' }`。解析顺序：

1. HTTP 非 2xx → `http` 错误（含 401/429/5xx）。  
2. body 为字符串 → 尝试 `JSON.parse`，失败则 `biz`「非法 JSON」。  
3. 若存在 `code` 字段且 `code !== 0` → `biz`，带上 `message`。  
4. 成功则返回 `data`（或兼容顶层 `reply`/`matches` 的旧契约）。

```ts
function unwrapEnvelope<T>(body: any): T {
  if (body && typeof body === 'object' && 'code' in body) {
    if (body.code !== 0) {
      const err: any = { type: 'biz', body, errMsg: body.message || '业务失败' }
      throw err
    }
    return body.data as T
  }
  return body as T
}
```

### 3. 错误 → UI 映射

| 类型 | 典型原因 | 用户文案 | 动作 |
| --- | --- | --- | --- |
| network | 断网/超时 | 网络不稳，请重试 | 重试按钮 |
| http 401 | Token 失效 | 登录已过期 | 清本地态 → 登录页 |
| http 429 | 限流 | 请求太频繁 | 退避后重试 |
| biz | code≠0 | 用服务端 message | 按业务码分支 |
| http 5xx | 服务异常 | 服务开小差 | 重试 + 上报 |

AI 对话：超时单独 `timeoutMs: 60000`；气泡错误态可重试；取消可用页面卸载时忽略回调（或自建 abort 标志）。与 Web 端共用错误码表（chat-core 常量），双端文案一致。

**业务例子**：doc-review-taro 的 `services/request.ts` 归一 `network|http|biz`；AI 生成与普通 CRUD 共用 client、不同 timeout。

### 4. 落地检查清单（口述可压缩）

1. **基址**：`BASE_URL` 分环境；真机不要写死局域网 IP 却忘配合法域名。  
2. **鉴权头**：统一 `authHeader()`，禁止业务页各自拼 Token。  
3. **超时分层**：CRUD 8s；导出/AI 生成 30–60s；超时错误文案与「取消」分开。  
4. **幂等与重试**：GET 可自动重试一次；POST 聊天消息用 clientMsgId 防重复发送。  
5. **日志**：开发环境打印 statusCode + 业务 code；生产只上报匿名错误码。  
6. **与 Nest 对齐**：同一 envelope；前端只信任 `code===0` 的 `data`，不把调试字段渲染进气泡。

这样封装后，面试能讲清「传输层错误 vs 业务错误 vs 可恢复错误」，而不是只说「用了 Taro.request」。

## 可能追问

- 要不要拦截器？→ 可以；请求侧灌 Token，响应侧 unwrap + 401 统一踢登。
- uploadFile 能否同一封装？→ 可同一错误模型，API 用 Taro.uploadFile，超时与进度条单独处理。
- 为何有时直接打 wx.request？→ 规避 Taro default/named 互操作坑；面试说清边界即可。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
