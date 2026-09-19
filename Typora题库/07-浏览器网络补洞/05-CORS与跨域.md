# 题 5：跨域为什么发生？CORS 怎么配？生产如何解？

## 面试官可能怎么问

- 同源策略判定？
- 简单请求和预检 OPTIONS？
- 开发代理与生产反代怎么做？

## 口述结构（90 秒）

1. 同源：协议+域名+端口
2. 浏览器限制前端读异源响应；服务器用 CORS 声明放行
3. 复杂请求先 OPTIONS；带 Cookie 时 Origin 不能是 *
4. 生产首选同域反代；JSONP 淘汰

## 参考答案

### 1. 同源策略

协议、主机、端口全相同才同源。  
`https://a.com` 与 `https://api.a.com` 不同源；端口不同也不同源。  
目的：防恶意站用你的登录态**读取**邮箱等接口结果。  
口径：请求常已发出，**没 CORS 时拦的是 JS 读响应**。

### 2. 简单请求 vs 预检

「简单方法 + 简单头 + 简单 Content-Type」可能直接发。  
出现 `Authorization`、`application/json`、`PUT/DELETE` 等 → 常先 **OPTIONS 预检**，通过后再发真实请求。

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Methods: GET,POST,PUT,OPTIONS
Access-Control-Max-Age: 86400
```

带 Cookie：`Allow-Origin` 必须具体源，**禁止 `*`**；前端 `credentials: 'include'`。

### 3. 解题顺序（步骤）

1. **同域反代（首选）**：浏览器只访问 `https://app.com/api`，Nginx 转内网 → 无跨域。  
2. **开发代理**：Vite `server.proxy` 模拟同上。  
3. **后端 CORS 白名单**：多域名、多端时配置。  
4. **JSONP**：仅 GET、弱错误处理、有 XSS 味——新项目不用。

```ts
// vite.config.ts 示意
server: {
  proxy: { '/api': { target: 'http://localhost:3000', changeOrigin: true } }
}
```

排障：看 OPTIONS 是否 204/200、Allow-Headers 是否包含自定义头、是否误用 `*` + credentials。

**业务例子**：AI 前端本地代理 Nest；生产网关同域。小程序是「合法 request 域名」，**不是**浏览器 CORS 语义——面试要主动对比。

### 4. 和小程序对比（加分）

| | 浏览器 CORS | 微信小程序 |
| --- | --- | --- |
| 谁限制 | 浏览器同源策略 | 平台合法域名白名单 |
| 预检 | OPTIONS | 无此模型 |
| 配置方 | 响应头 / 网关 | 小程序后台 + HTTPS |
| 本地 | 开发代理 | 开发工具勾选不校验 |

排障口诀：H5 跨域先看响应头与是否该同域；小程序失败先看域名配置与 TLS。  
不要把「小程序请求失败」答成「没配 CORS」——这是高频扣分点。

补充：`*` 通配 Origin 不能与 `Credentials` 同用；多环境用白名单数组匹配 `Origin`。

## 可能追问

- CORS 防 CSRF 吗？→ 不防。
- 预检被缓存？→ Max-Age；改头后注意清。
- 跨域带 Cookie 登录？→ 前后端同时开 credentials + 明确 Origin + SameSite 策略。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
