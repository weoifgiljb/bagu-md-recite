# 题 13：AI 功能的鉴权：Token、DemoTokenGuard、密钥位置？

## 面试官可能怎么问

- API Key 能放前端吗？
- DemoTokenGuard 类机制前端怎么配合？
- 如何避免 Token 进仓库？

## 先自己答（90 秒）

## 参考答

**铁律**：模型供应商密钥、云密钥**只放服务端**；前端只有「用户会话 / 演示令牌」，权限由后端收敛。

**前端配合**
- 登录或演示入口领取 short-lived token → 内存优先，必要时 httpOnly cookie
- 请求 AI 接口带 `Authorization`；401 走刷新或重新获取 Demo Token
- `.env` 里只放公钥类配置（API Base URL）；**禁止**提交 `OPENAI_API_KEY`
- CI/预发用密钥管理，不把 token 写进示例 md/截图

**DemoTokenGuard（概念）**
- 后端校验演示令牌后才允许 `POST /api/ai/chat`
- 前端负责：拿到 token、过期提示、未携带时的引导 UI
- 演示环境可配合 lab 开关；仍不能把供应商主密钥下发

**业务例子**：Nest 守护 AI 路由；小程序与 Web 共用同一鉴权头约定；AdminJS 另用管理员会话，和 C 端 Demo Token 分离。

## 可能追问

- Token 会不会被 XSS 偷？→ 减少长命 token 在 localStorage；配合 CSP/消毒。
- 多端共用？→ 同一账户体系统一签发；小程序可能另有 code2session。

## 我的四行

- 定义：
- 原理：
- 业务例子：
- 可能追问：
