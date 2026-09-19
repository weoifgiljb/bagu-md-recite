# 题 6：CSP 对防 XSS 有什么帮助？前端要知道哪些头？

## 面试官可能怎么问

- CSP 是什么？
- 为什么还要 CSP？
- 常见安全响应头还有哪些？

## 口述结构（90 秒）

1. CSP：浏览器按策略决定能不能加载/执行脚本等
2. 即使漏了转义，也能挡住很多内联与异源脚本
3. 前端要配合：少内联脚本、用 nonce/hash
4. 还有 Cookie 标志位、X-Frame-Options/XFO 替代 frame-ancestors 等

## 参考答案

### 1. CSP 是什么

Content-Security-Policy 是 HTTP 响应头（或 meta，能力较弱）。  
浏览器按策略限制：脚本源、样式源、图片源、`eval`、是否允许内联等。

```http
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'
```

步骤落地：  
1. 预发先用 `Content-Security-Policy-Report-Only` 收集报告  
2. 修违规（内联脚本改外链或加 nonce）  
3. 再切 enforce  

### 2. 为什么还要 CSP（多层防御）

转义/消毒可能漏；CSP 是**第二道闸**：异源脚本、未加 nonce 的内联脚本直接拒执行。  
前端配合：构建时注入 nonce；避免 `eval`、字符串 `setTimeout`；第三方脚本进白名单。

### 3. 前端应认识的安全头

| 头 | 作用 |
| --- | --- |
| Content-Security-Policy | 资源/脚本策略 |
| Set-Cookie 的 HttpOnly/Secure/SameSite | 会话防盗与 CSRF 面 |
| Referrer-Policy | 少泄露来源 URL |
| Permissions-Policy | 关摄像头/地理等 |
| X-Content-Type-Options: nosniff | 减 MIME 嗅探 |
| frame-ancestors / X-Frame-Options | 防被嵌 iframe 点击劫持 |

前端面试不要求背全语法，但要会说：**CSP 防 XSS 补位；SameSite/CSRF token 防跨站请求；HttpOnly 降 token 被 JS 读。**


### 4. 和前端构建的关系

Vite/Webpack 打包后脚本文件名带 hash，正好适配 `script-src 'self'`。  
内联的运行时注入（如主题脚本）要改成外链或 `nonce`。  
第三方 SDK（统计、客服）必须进白名单，否则一开 CSP 就全挂——这是上线前要用 report-only 的原因。

## 可能追问

- meta CSP 的限制？→ 不能限制所有指令（如 frame-ancestors）。  
- 开发环境 CSP 太严？→ 用 report-only 或开发放宽、生产收紧。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
