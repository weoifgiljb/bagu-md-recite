# 题 8：小程序 AI Tab 信息架构怎么设计（列表/会话/匹配文档）？

## 面试官可能怎么问

- AI Tab 里信息怎么分层？
- 文档列表、会话、匹配结果如何导航？
- 页面栈过深怎么避免？

## 口述结构（90 秒）

1. Tab 分：文档 / AI / 我的；AI 默认进助手会话壳
2. 会话内消息 + 回答下挂 matches；点 match 进详情
3. 筛选状态与 conversationId 进全局/Storage
4. 控制栈深：详情 navigateTo，回会话 navigateBack；忌一层堆所有

## 参考答案

### 1. 推荐信息架构

- **Tab·文档**：列表 + 筛选（状态/关键词）；进详情。  
- **Tab·AI**：助手首页/当前会话；输入框 + 消息列表。  
- **回答卡片**：文案 + **匹配文档 matches**（标题/分数/摘要）。  
- **文档详情**：从列表或 match 进入；可再回会话。  
- **我的**：登录态、设置、关于。

原则：**会话态**与**文档库浏览态**分开；不要在一个 scroll 里塞「全库 + 全历史 + 详情」。

### 2. 导航与状态步骤

1. AI Tab 用 `switchTab` 进入，避免栈上叠多个 AI 根页。  
2. 会话 → 详情：`navigateTo('/pages/detail/index?id=')`。  
3. 详情返回：`navigateBack`，会话滚动位置尽量保留（组件态或手动记 scrollTop）。  
4. 全局存：`conversationId`、进行中的 `pending`、文档筛选条件。  
5. matches 点击带齐 `docId`，详情页 `onLoad` 拉全文/批注。

```ts
// 伪结构
type ChatState = {
  conversationId: string
  messages: Array<{ role: 'user'|'assistant'; content: string; matches?: Match[] }>
  pending: boolean
}
```

### 3. 性能与分包

- 历史消息分页；视图层只挂最近 N 条。  
- 富文本/高亮进 AI 相关分包或懒加载。  
- setData 只更新当前气泡（见题 1）。  
- 非流式契约先跑通，再评估 WS。

**业务挂载**：doc-review-taro 的 tab（首页/文档/AI/我的）+ ChatWidgets + docs list/filter；面试强调「信息架构先于组件炫技」。

### 4. 状态机与空态

会话建议显式状态：`idle | sending | streaming | error`。  
- `idle`：可输入。  
- `sending`：用户消息已上屏，助手占位气泡。  
- `error`：气泡可重试，不丢用户原文。  

空态文案引导「问问某份文档」「从文档 Tab 选一篇再来」。  
从 match 进详情再返回，应回到**同一会话**而非新建——靠 `conversationId` 持久化。  
若产品有「文档审评 + AI」，列表筛选与 AI 引用文档要用同一套 docId，避免两套主键。

**验收口述**：tab 切换不丢会话；栈深可控；matches 可点进详情；弱网有错误态与重试。

## 可能追问

- 列表很长？→ 分页；会话与文档状态分仓。
- 是否一页堆全部？→ 不建议，栈、性能、分包都差。
- H5 同构？→ 路由可用同一信息架构，能力降级单独表。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
