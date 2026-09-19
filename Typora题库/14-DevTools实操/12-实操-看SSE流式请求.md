# 题 12：实操——AI 对话流式（SSE/fetch stream）在 Network 里怎么看

## 面试官可能怎么问

- 流式接口和普通 JSON 在 Network 里有什么不一样？
- 中途点停止，你期望看到什么状态？
- 一顿一顿出来或最后才刷，可能是什么原因？

## 口述结构（90 秒）

1. 滤 Fetch/XHR，发一条消息，找长时间 pending 的请求
2. 看 Type、Status 200、Response 是否逐步出现 data
3. 停止生成应对应 canceled / 流结束
4. 若整块延迟：查代理缓冲；卡顿另开 Performance

## 参考答案

### 操作步骤（照着点）

1. F12 → **Network** → **Fetch/XHR**，勾选 **Preserve log**。
2. Clear 后，在页面 **发送一条会流式返回的消息**。
3. 找 Name 像 `/chat`、`/completions`、`/sse` 的请求；特征是：
   - Status **200** 后，Time 一直走，行上可能一直 **pending**
   - Type 可能是 **eventsource**、**fetch**、**xhr**
4. 点开 → **Headers**：
   - `Content-Type` 是否 `text/event-stream` 或仍是 `application/json`（fetch 流式不一定是 SSE 类型）
   - 请求是否带 Authorization
5. 打开 **Response / EventStream**（有的 Chrome 版本在 Response 里陆续刷 `data:` 行）：
   - 正常：一边生成一边多行 `data:`
   - 异常：一直空，最后才整包出现 → 怀疑 **Nginx/网关缓冲**（面试可提 `proxy_buffering off`）
6. 点页面 **停止生成**：
   - Network 里该请求变为 **canceled**（前端 AbortController）或结束
   - 若一直挂着：查前端有没有 abort，或后端没关连接
7. 若「网络在流，但页面卡」：再开 **Performance** 短录，看是否每个 token 重渲染整列表（回扣题 10）。

### 和普通接口对照表

| | 普通 JSON | 流式 |
|--|-----------|------|
| 耗时 | 一次结束 | 长时间 pending |
| Response | 一次性 JSON | 多段 data / chunk |
| 取消 | 较少 | 常见 canceled |

## 可能追问

- EventSource 为什么很少用于带 Token 的对话？→ 难自定义 Header，多用 fetch + ReadableStream。
- 如何确认是前端没读流还是后端没推？→ Response 有数据但 UI 不动 = 前端解析/渲染；Response 也空 = 链路或后端。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [SSE 与流式输出](../03-AI前端/SSE与流式输出.md)
- [WS / SSE / HTTP 选型](../03-AI前端/WebSocket与SSE与HTTP选型.md)
- [取消与断线重连](../03-AI前端/请求取消与断线重连.md)
- [限流 429 与重试](../03-AI前端/限流429与超时重试.md)
- [JS：服务器发送事件](../01-JavaScript/06-DOM事件与浏览器API/什么是服务器发送事件？.md)
