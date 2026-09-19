# 题：RAG 链路里前端职责是什么？和后端怎么切？

## 面试官可能怎么问

- 检索式助手的前端主路径是什么？
- pending / phase / searchMatches 状态怎么设计？
- 前端绝不该做什么？

## 口述结构（90 秒）

1. 主路径：提问→检索/生成中→matches+reply→点开文档
2. 状态与 messages 解耦：matches 挂在该条 assistant 上
3. 前端负责展示、跳转、空态、可追溯；不做私有向量检索
4. 无真 LLM 也按同一契约开发

## 参考答案

### 对应问 1：前端主路径

1. 用户提问 → UI `pending`（可细分为 searching / answering）
2. 后端检索（关键词/向量）+ 生成 → 返回 `matches` + `reply`
3. UI 展示 matches → 用户点击打开 Doc（带 `docId`/锚点）
4. 可选：在 Doc 内追问（缩小检索范围到当前 doc）

对齐项目：即使后端是演示检索、**非真 LLM**，前端仍按此路径，保证「可点开的依据」。

### 对应问 2：状态设计

```ts
type Phase = 'idle' | 'searching' | 'answering' | 'done' | 'error'
// message 上：
{ role: 'assistant', reply, matches: Match[], phase, error? }
```

要点：
- `searchMatches` **挂在该条消息**，不要全局唯一一份（避免串台）
- `pending` 可用 `phase !== idle && !== done`
- 取消：AbortController；忽略过期响应（请求世代号）

### 对应问 3：前端绝不该做什么

| 该做 | 不该做 |
| --- | --- |
| 展示 matches、跳转、高亮、空态文案 | 浏览器里跑私有向量库当生产检索 |
| 引用可点击、无依据弱提示 | 伪造脚注 offset 假装精确引用 |
| 鉴权头走约定、密钥不进包 | 把 Admin Token 打进小程序/前端包 |
| 超时/429 提示与重试 | 静默吞错继续「一本正经胡说」 |

**业务例子**：文档审评 `POST /api/ai/chat` → `{ reply, matches }`；列表点进详情核实条款。


## 可能追问

- 无结果？→ 空态：换关键词 / 引导上传 / 缩小范围。
- search 与 chat 同一 API？→ 可合并返回；或先 search 再 answer，UI 都要能讲。
- 流式 RAG？→ 先流式 reply，matches 可后到；或先骨架 matches 再填字。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
