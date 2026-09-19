# 题 7：CSRF 是什么？和 XSS、Cookie 有啥关系？（前端视角）

## 面试官可能怎么问

- CSRF 原理？
- SameSite 有什么用？
- token 放 Header 为什么更常见？

## 口述结构（90 秒）

1. CSRF：借受害者已登录的浏览器，向目标站发「受害者意图外」的请求
2. 依赖：浏览器自动带 Cookie
3. 防：SameSite Cookie、CSRF Token、关键操作不用纯 Cookie 鉴权
4. 和 XSS 不同：CSRF 不需注入脚本，但 XSS 可绕更多防线

## 参考答案

### 1. CSRF 原理（步骤）

1. 用户已登录 `bank.com`，会话 Cookie 还在  
2. 用户打开恶意站 `evil.com`  
3. 恶意页触发对 `bank.com` 的请求（表单/图片/fetch）  
4. 浏览器**自动带上** bank 的 Cookie  
5. 若服务端只认 Cookie、无额外校验 → 转账等写操作被伪造  

关键：攻击者**不一定能读到响应**（受同源限制），但可能成功「写出操作」。

### 2. SameSite 有什么用

Cookie 属性 `SameSite=Lax|Strict|None`：

- **Strict**：跨站请求基本不带 Cookie（最严，可能影响部分跳转登录体验）  
- **Lax**：常见导航 GET 带；跨站 POST 等不带——能挡一批 CSRF  
- **None**：跨站也带，必须 `Secure`；第三方场景才用  

步骤：会话 Cookie 默认至少 `SameSite=Lax` + `Secure` + `HttpOnly`；再叠加 CSRF token 更稳。

### 3. token 放 Header 为什么更常见

CSRF token / JWT 放自定义头（如 `Authorization`、`X-CSRF-Token`）：  
- 简单表单/图片请求**不会自动带自定义头**  
- 跨站恶意页除非 CORS 放开（正确配置下不会），否则读不到你的 token  

对比：只靠 Cookie 的会话，浏览器会自动附带，才有 CSRF 面。  
现代 SPA 常见：`Authorization: Bearer <access>`（存内存或稳妥方案）+ 刷新令牌策略；若仍用 Cookie 会话，则必须 SameSite + CSRF 方案。

和 XSS：XSS 可偷非 HttpOnly 的 token，或直接以用户身份调 API——**CSP/消毒与 CSRF 防护要一起讲**。

## 可能追问

- GET 会有 CSRF 吗？→ 若服务端用 GET 做写操作就会；规范上写操作应用 POST/PUT 并校验。  
- 双重 Cookie 方案？→ 前端读 Cookie 再回传 Header，与 SameSite 组合使用。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
