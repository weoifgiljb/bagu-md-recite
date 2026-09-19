# 题 8：跨域为什么发生？CORS 和 JSONP？

## 面试官可能怎么问

- 同源策略是什么？
- 简单请求和预检？
- 生产怎么解跨域？

## 口述结构（90 秒）

1. 同源：协议+域名+端口一致
2. 浏览器限制「前端读异源响应」，防数据被偷
3. CORS 由服务器声明放行；复杂请求先 OPTIONS
4. 生产优先同域反代；JSONP 基本淘汰

## 参考答案

### 1. 同源策略是什么

判定：协议、主机名、端口全部相同才同源。  
例如 `https://a.com` 与 `https://a.com:443` 通常同；`https://a.com` 与 `https://api.a.com` **不同源**。  

目的：避免恶意站点用你的登录态去读邮箱/网银接口结果。  
注意口径：很多时候请求在网络上已经发出，**浏览器拦住的是 JS 读取响应**（没 CORS 时控制台报跨域）。

### 2. 简单请求和预检

满足「简单方法 + 简单头 + 简单 Content-Type」时，浏览器可能直接发真正请求。  
一旦出现自定义头（如 `Authorization`）、`application/json`、`PUT/DELETE` 等，往往先发 **OPTIONS 预检**，通过后再发实际请求。

服务端需要正确响应：

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Methods: GET,POST,PUT,OPTIONS
```

若要带 cookie：`Allow-Origin` 必须是具体源，**禁止 `*`**，前端 `credentials: 'include'`。

### 3. 生产怎么解跨域（推荐顺序）

1. **同域反代**（首选）：浏览器只访问 `https://app.com/api/...`，Nginx 转到内网服务 → 无跨域  
2. **开发代理**：Vite/Webpack `proxy` 模拟同上  
3. **后端 CORS 白名单**：多端、多域名时配置允许的 Origin  
4. **JSONP**：用 `<script>` 绕过（仅 GET、回调函数名、错误处理弱、有 XSS 风险）——新项目不要用  

步骤（本地联调）：配 Vite proxy → 确认请求路径变成相对 `/api` → 上线改为网关同域。

### 4. 业务例子

AI 前端本地代理 Nest；生产 Nginx 反代。小程序则是「合法 request 域名」白名单，不是浏览器 CORS 语义。

## 可能追问

- CORS 能防 CSRF 吗？→ 不能；CSRF 靠 SameSite/Token。  
- 预检失败怎么排？→ 看 OPTIONS 是否 204/200、Allow-Headers 是否包含你的自定义头。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
