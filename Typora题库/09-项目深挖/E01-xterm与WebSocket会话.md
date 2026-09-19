# 题 13：Web 终端：xterm 与 WebSocket 的职责、世代和重连怎么讲？

## 面试官可能怎么问

- xterm 和 WS 各干什么？
- 旧连接晚到的输出怎么处理？
- restored/replayed/new 是什么？

## 口述结构（90 秒）

1. xterm：渲染与本地输入；WS：字节流与信令
2. session 稳定，conn 可断；连接世代号丢弃旧输出
3. restored / replayed / new 区分回放与新会话
4. 监控大列表：聚合 + 虚拟列表，不一次灌 DOM

## 参考答案

### 对应问 1：职责划分

| 组件 | 职责 |
| --- | --- |
| xterm.js | 终端渲染、本地键盘/粘贴、滚动缓冲 |
| WebSocket | 与后端 PTY/代理的字节流、会话信令（resize、鉴权、心跳） |

步骤（输入）：
1. 用户按键 → xterm `onData`
2. 若已 attach → WS 发送；未 attach → 入队或按策略丢弃（说清）
3. 服务端输出 → WS message → `term.write`

### 对应问 2：旧连接晚到的输出

1. 每次建立连接 `connGen++`
2. 消息处理前校验 `gen === 当前`
3. **旧连接晚到的输出整包丢弃**，避免串台（A 会话的字打到 B）

重连：
1. 断线提示 + 指数退避重连（带 jitter）
2. 新连接认证 / attach session
3. 按服务端指示走 replay 或 new

### 对应问 3：restored / replayed / new

- **restored**：会话仍在，前端状态恢复
- **replayed**：服务端回放缓冲，补历史输出
- **new**：全新会话，清屏或新 tab

**监控页旁路**：2000+ 硬件点 → 聚合指标 + 虚拟列表/分页，**禁止一次灌 DOM**。


## 可能追问

- resize？→ 容器 ResizeObserver → 算 cols/rows → WS 发 resize 信令。
- ANSI 半包？→ 连接层拼缓冲，按完整序列再 write；或交给 xterm 流式喂。
- 权限失效？→ 服务端关连接；前端锁输入 + 提示重新授权。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
