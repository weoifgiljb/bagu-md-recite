# 题 15：Vue3 与 React 双栈做同一 AI 页时的共性抽象？

## 面试官可能怎么问

- 哪些东西可以抽成框架无关？
- stream parser、message model、renderer 怎么分层？

## 先自己答（90 秒）

## 参考答

**可共享（框架无关）**
1. **Message model**：类型定义（role/content/status/id）
2. **Stream parser**：把 SSE/fetch bytes → 增量事件（`text-delta`/`error`/`done`）
3. **API client**：fetch 封装、错误 envelope、取消
4. **Sanitize / markdown pipeline**：输入字符串 → 安全 HTML/AST

**框架层各自实现**
- Vue：Pinia store + 组件
- React：Context/Zustand + 组件
- Taro：再包一层 `setData` 适配

**渲染器**
- `MessageList` / `MessageBubble` / `MatchesPanel` 看齐 props 协议
- 打字机与虚拟列表属 UI 适配，可共享「节流策略」而非 DOM 代码

**业务例子**：简历 Vue3 站 + doc-review-taro React 小程序；面试强调「协议与解析共享，UI 各写」降低维护成本。

## 可能追问

- Monorepo 怎么放？→ `packages/chat-core` 纯 TS，别依赖 Vue/React。
- SSR？→ parser 可同构；注意 window 依赖隔离。

## 我的四行

- 定义：
- 原理：
- 业务例子：
- 可能追问：
