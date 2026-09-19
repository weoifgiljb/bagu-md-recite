# 题 1：SSE / 流式输出是什么？前端怎么接？

## 面试官可能怎么问

- SSE 和 WebSocket、普通 HTTP 有什么区别？
- 浏览器里怎么消费 `text/event-stream`？
- 和 `fetch` + `ReadableStream` 方案怎么选？
- 流式过程中如何更新 UI 又不卡顿？

## 先自己答（90 秒）

> 闭卷说：定义 → 怎么接 → 和业务聊天页的关系 → 一个坑

## 参考答（可上嘴版）

**定义**：服务端把模型输出按 chunk 持续推给前端；前端边收边渲染，降低首字等待。

**常见实现**
1. **SSE（EventSource / fetch 读 stream）**：单向（服务端 → 客户端），适合「生成回答」
2. **WebSocket**：双向，适合协作、实时编辑；聊天生成用 SSE 通常更简单
3. **普通一次性 JSON**：等整段结束才返回，首包慢，面试里要会对比

**前端怎么接（fetch + ReadableStream 思路）**
- `fetch(url, { signal })`
- `res.body.getReader()` + `TextDecoder`
- 按行/按 SSE 事件解析 `data:`
- 把增量 append 到当前消息的 `content`

**业务挂载**：你做 AI 对话页时，用户点发送 → 先插入一条 assistant 占位 → 流式追加文字 → 结束标记 `done` 后落库/允许重新生成。

**常见坑**
- 代理/Nginx 缓冲导致「一会儿来一大截」：要关 buffering 或用正确 headers
- 解析半包：chunk 边界不一定在行尾，要缓冲区拼行
- 错误帧：区分网络断了 vs 模型报错事件

## 可能追问

- 为什么很多项目不用 `EventSource`？→ 不好自定义 Header（如 Authorization），所以常用 fetch stream
- POST 能不能 SSE？→ EventSource 基本是 GET；要 POST 用 fetch stream

## 我的四行

- 定义：
- 原理：
- 业务例子：
- 可能追问：
