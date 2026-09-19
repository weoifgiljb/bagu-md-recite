# 题 9：实操——抓一条登录/业务接口，用 Copy as cURL 对照

## 面试官可能怎么问

- 你怎么证明问题在前端封装还是后端？
- Copy as cURL 之后你具体做什么？
- 敏感 Token 怎么处理？

## 口述结构（90 秒）

1. Network 过滤 Fetch/XHR，Preserve log，复现一次登录或发消息
2. 点开请求看 Status / Request Headers / Payload / Response
3. 右键 Copy as cURL，终端跑通则后端 OK
4. 打码 Authorization 再贴给同事

## 参考答案

### 操作步骤（照着点）

1. 打开要测的页面，按 **F12** → **Network**。
2. 勾选 **Preserve log**、**Disable cache**；过滤选 **Fetch/XHR**。
3. 点面板左上角禁止图标 **Clear**，保证列表是空的。
4. 在页面上 **只做一次** 目标操作（登录 / 发送 / 保存）。
5. 在列表里找到对应请求（看 Name 路径，如 `/api/login`、`/auth/token`）。
6. 点击该行，右侧按顺序看：
   1. **Headers → General**：Method、Status、URL
   2. **Request Headers**：有没有 `Authorization: Bearer ...` 或 Cookie
   3. **Payload**（或 Request）：账号字段、JSON 是否正确
   4. **Preview / Response**：业务 code、message、token 字段
7. 在该行 **右键 → Copy → Copy as cURL**。
8. 打开终端粘贴执行（Windows 可用 Git Bash / WSL；或 Copy as fetch 在 Console 跑）。
9. **对照结论**：
   - cURL 也是 401/500：优先查后端/网关/环境变量，不是 axios 拦截器写错那么简单。
   - cURL 200，页面失败：查前端 baseURL、拦截器改写、是否看错环境、是否被 CORS 拦（浏览器里 failed、cURL 正常很常见）。
10. 把 cURL 发给别人前：**删掉或打码** `Authorization`、Cookie、密码字段。

### 你要练到的肌肉记忆

- 一张图能说清：URL + Status + 关键请求头 + 响应第一屏。
- 会用 Initiator 点到发请求的源码行（同面板右侧 Initiator）。

## 可能追问

- Copy as fetch 和 cURL 差别？→ fetch 方便在 Console 带 cookie 同源试；cURL 方便脱离浏览器测服务端。
- 为什么浏览器 CORS failed，cURL 却通？→ cURL 不受浏览器同源策略限制。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [接口请求怎么排查](04-接口请求怎么排查.md)
- [AI 功能鉴权](../03-AI前端/AI功能鉴权.md)
- [fetch 与 axios](../12-BOM-DOM-Ajax/07-fetch与axios.md)
- [Taro.request 对接](../06-Taro小程序/Taro-request对接Nest-AI.md)
