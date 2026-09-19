# 题 7：AI Chat API 契约：请求/响应字段与前端怎么用？

## 面试官可能怎么问

- 设计一个 Chat API，请求和响应里通常有哪些字段？
- envelope / 错误码怎么约定？前端怎么统一处理？
- 结合 Nest `POST /api/ai/chat` 返回 `{ reply, matches }`，前端怎么渲染？

## 先自己答（90 秒）

## 参考答

**契约目标**：前后端对「成功长什么样、失败长什么样、业务数据在哪」达成一致，UI 才能稳定。

**常见请求字段**
- `message` / `messages`：本轮用户输入或完整消息数组
- `conversationId`：会话续写（没有则新建）
- `clientMessageId`：幂等，防重复提交
- 可选：`docIds`、检索范围、`stream: true`、实验室 delay 开关

**常见响应（非流式）**
- 业务体：如 `{ reply: string, matches: Array<{ id, title, snippet?, score? }> }`
- 或统一 envelope：`{ code, message, data }`；成功时 `data` 里才是 reply/matches

**Nest 示例怎么用（对齐 doc-review-functions）**
1. 前端带 Demo/用户 Token（Header），打 `POST /api/ai/chat`
2. 解析 JSON：把 `reply` 写入 assistant 气泡
3. 若 `matches` 非空：旁路/底部渲染「相关文档」列表，点击跳转文档详情
4. 若 matches 空且产品要求「可追溯」：展示拒答或弱提示文案，而不是假装很懂

**错误码前端约定**
- `401/403`：鉴权失败 → 引导重新拿 Demo Token / 登录
- `429`：限流 → 倒计时重试文案
- `4xx` 业务：展示 `message`，不要只 toast「请求失败」
- `5xx` / 超时：可重试 + 保留用户输入

**业务例子**：当前后端可能是关键词/统计检索 Docs，尚未真 LLM；前端仍应按「reply + matches」契约开发，以后换成真模型时 UI 不用翻掉。

## 可能追问

- 流式时契约怎么变？→ 事件：`delta` / `matches` / `done` / `error`；matches 可在结束帧一次性给。
- 为什么要 clientMessageId？→ 弱网重试时避免插入两条用户消息。
- DemoTokenGuard 失败前端怎么表现？→ 明确「演示令牌无效/过期」，不要当成模型答不出。

## 我的四行

- 定义：
- 原理：
- 业务例子：
- 可能追问：
