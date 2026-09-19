# 题 3：CSRF 是什么？和 Cookie、SameSite、XSS 的关系？

## 面试官可能怎么问

- CSRF 攻击步骤？
- SameSite=Lax/Strict/None 怎么选？
- Token 放 Header 为何能减轻 CSRF？

## 口述结构（90 秒）

1. CSRF：借用已登录浏览器，发受害者非本意的请求
2. 根子是浏览器自动带 Cookie
3. 防：SameSite、CSRF Token、关键操作不用纯 Cookie
4. XSS 可偷 token/以用户身份调 API，需一起防

## 参考答案

### 1. 攻击步骤

1. 用户登录 `bank.com`，会话 Cookie 仍有效。  
2. 用户访问 `evil.com`。  
3. 恶意页自动发起对 `bank.com` 的写请求（隐藏表单 POST、图片、fetch）。  
4. 浏览器**自动附带** bank Cookie。  
5. 服务端若只认 Cookie、无额外校验 → 转账/改密等被伪造。  

攻击者未必读到响应（同源拦读），但「写出」可能已成功。

### 2. SameSite 与 Cookie 属性

- **Strict**：跨站基本不带 Cookie，最严。  
- **Lax**：顶层导航 GET 可带；跨站 POST 等不带——挡一批 CSRF。  
- **None**：跨站也带，必须 `Secure`；第三方场景才用。  

再叠加：`HttpOnly`（防 JS 读）、`Secure`（仅 HTTPS）。  
步骤：会话 Cookie 至少 `SameSite=Lax; Secure; HttpOnly`；高风险再加 CSRF Token。

### 3. Header Token 方案

把 CSRF token 或 JWT 放自定义头（`Authorization` / `X-CSRF-Token`）：  
简单表单/图片**不会自动带**自定义头；恶意站也读不到你的 token（CORS 正确时）。  

```http
Authorization: Bearer <access_token>
```

现代 SPA：Bearer 存内存或稳妥方案 + 短过期；若仍用 Cookie 会话，必须 SameSite + CSRF 双保险。  
和 XSS：XSS 可绕过许多 CSRF 防线——**消毒/CSP 与 CSRF 要一起讲**。

**业务例子**：管理后台 Cookie 会话开 SameSite；小程序主用 Header Token，CSRF 面更小，但仍要防 XSS 与越权。

### 4. 选型决策树

1. 鉴权是否主要靠 **Cookie 会话**？  
   - 是 → SameSite + CSRF Token（同步表单）或双重 Cookie；关键操作再验证。  
   - 否，纯 **Bearer Header** → CSRF 面大幅下降，仍要防 XSS 偷 Token。  
2. 是否跨站嵌入（第三方 iframe）？  
   - 需要 Cookie → `SameSite=None; Secure`，并评估风险。  
   - 不需要 → 避免 None。  
3. 是否与移动端/小程序共用 API？  
   - 统一走 Header Token 往往更清晰。  

口述金句：**CSRF 骗的是浏览器自动带的身份；XSS 偷的是页面里能碰的身份。**

## 可能追问

- GET 会有 CSRF 吗？→ 若 GET 有副作用就会；写操作应用 POST/PUT + 校验。
- 双重 Cookie？→ 前端读 Cookie 再回传 Header，配合 SameSite。
- CORS 能防 CSRF 吗？→ 不能；CORS 管的是读响应，不是自动带 Cookie 的写。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
