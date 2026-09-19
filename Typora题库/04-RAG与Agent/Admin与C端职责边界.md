# 题：Admin/运营侧与 C 端 AI 助手的职责边界？

## 面试官可能怎么问

- 对话日志、文档状态机放哪边？
- AdminJS 和 C 端 Chat 如何分工？
- 边界原则有哪些硬规矩？

## 口述结构（90 秒）

1. C 端：提问、看回复与 matches、打开文档、轻量历史
2. Admin：审计日志、文档状态机、限流与模型路由、敏感处理
3. C 端不直接改索引/权限；Admin 操作留 DocEvent
4. 密钥与 DemoToken 配置在服务端，不进前端包

## 参考答案

### 对应问 1：日志与状态机放哪边

| 能力 | 归属 |
| --- | --- |
| 提问、流式/非流式回复、matches、打开文档、上传（若开放） | **C 端** |
| 对话日志审计、敏感词/滥用处理 | **Admin** |
| 文档状态：上传→解析→可检索→下架 | **Admin + 后端状态机** |
| Demo Token、限流、lab delay、模型路由 | **Admin/配置中心** |

C 端只读「可检索」文档；下架后 matches 应失效或提示下架。

### 对应问 2：AdminJS vs C 端 Chat

步骤（文档审评例子）：
1. 运营在 AdminJS 管 Doc / Comment / DocEvent（Prisma 模型可视）
2. Nest 提供 `POST /api/ai/chat` 与文档只读 API
3. Taro/Web C 端只消费助手与只读文档，**不暴露** Admin 路由

Comment ≠ Chat：Comment 是文档协作；Chat 是助手会话。

### 对应问 3：硬规矩

1. C 端**不直接改**索引、权限、全局 Prompt
2. Admin 写操作留 **DocEvent/审计**
3. 日志默认脱敏；生产看完整回复需权限
4. 密钥、Admin Cookie、DemoToken **不进**小程序/前端包
5. 运营想「改模型回复」→ 谨慎；更好是标注 + 再生成策略，而不是默默篡改历史当真

**业务例子**：Nest + Prisma + AdminJS 管 Doc；C 端只打 chat 与文档详情。


## 可能追问

- C 端要看自己的历史？→ 轻量历史 API，按用户隔离；不是 Admin 审计页。
- 解析失败文档？→ Admin 看状态与重试；C 端不可检索。
- 多租户？→ Admin 按租户隔离；C 端 Token 带租户声明。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
