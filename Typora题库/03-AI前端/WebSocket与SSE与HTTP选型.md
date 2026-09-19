# 题 6：WebSocket vs SSE vs 普通 HTTP：AI 产品怎么选？

## 面试官可能怎么问

- 聊天生成、协作编辑、终端类双向通道，通信方式怎么选？
- SSE 和 WebSocket 各自适合什么？什么时候普通 HTTP 就够？
- xterm.js / 远程终端为什么通常选 WebSocket？

## 先自己答（90 秒）

## 参考答

**一句话选型**：生成型对话优先 **SSE（或 fetch 流）**；需要双向实时协作用 **WebSocket**；一次问一次答、延迟可接受用 **普通 HTTP JSON**。

**对比表（面试口述）**
- **普通 HTTP**：请求 → 等完整响应 → 结束。实现最简单，适合非流式 Chat、检索接口、Admin 操作。首包慢、无法中途停止（除非另开取消通道）。
- **SSE / fetch ReadableStream**：服务端 → 客户端单向持续推送。适合「模型边生成边出字」。HTTP 语义清晰，代理友好；要自定义 Header（Authorization）时常用 `fetch` + stream，而不是裸 `EventSource`。
- **WebSocket**：全双工。适合多人协作光标、协同编辑、游戏状态、**xterm 交互式终端**（键入与输出都是高频双向）。聊天生成也能用，但要自己处理心跳、重连、帧协议，复杂度高于 SSE。

**AI 产品常见组合**
1. **聊天生成**：SSE / fetch stream（TTFT 体验）；停止用 `AbortController` + 可选后端 cancel。
2. **文档审阅助手返回 matches**：即便非流式，一次 HTTP 返回 `{ reply, matches }` 也够用；以后再升级流式。
3. **协作 / 在线 IDE / xterm.js**：WebSocket；终端里 stdin/stdout/resize 都是双向事件。
4. **通知类**：SSE 或 WebSocket 均可；若已有 WS 通道可复用。

**业务挂载**：简历站若列 WebSocket/xterm.js，面试时说清「终端/协作用 WS；对话生成用 SSE/HTTP」——不要把所有实时都说成 WebSocket。

**坑**：反向代理缓冲会把 SSE「攒一大截再吐」；WS 要处理心跳与鉴权（子协议 / 首包 token）；小程序对 WS/SSE 支持与域名校验更严（另题）。

## 可能追问

- 为什么很多 ChatGPT 类产品不用 EventSource？→ 难带自定义 Header，POST 也不友好，故 fetch stream。
- 同一产品能否混用？→ 可以：对话 SSE，协作 WS，CRUD 仍用 REST。
- HTTP/2 或 HTTP/3 下 SSE 还要不要？→ 仍常用；流式语义比传输层版本更关键。

## 我的四行

- 定义：
- 原理：
- 业务例子：
- 可能追问：
