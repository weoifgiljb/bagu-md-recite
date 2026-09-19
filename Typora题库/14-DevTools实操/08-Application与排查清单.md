# 题 8：Application 面板怎么用？白屏/接口挂/页面卡的排查清单？

## 面试官可能怎么问

- Token 存在哪？怎么清站点数据？
- Service Worker 怎样导致「怎么清缓存都旧」？
- 给我一套前端排障顺序。

## 口述结构（90 秒）

1. Application：Storage / Cookies / Cache / SW
2. 清数据与 Bypass SW 的步骤
3. 三类故障各三步：白屏、接口、卡顿
4. 强调：先复现，再开对应面板，再留证据（截图/cURL）

## 参考答案

### 1. Application 常用

1. **Local Storage / Session Storage**：看业务 key、Token（注意别在共享屏幕暴露）。
2. **Cookies**：域名、HttpOnly（HttpOnly 在 Application 可见但 JS 读不到）、Expires、SameSite。
3. **Cache Storage**：PWA/SW 缓存的请求。
4. **Service Workers**：状态、Update、Unregister。
5. 左上 **Clear site data**：一键清存储+缓存（核按钮，清前先打住现场）。

### 2.「怎么刷新都是旧的」

1. Network → Disable cache，硬刷新。
2. Application → Service Workers → 勾选 **Bypass for network** 或 Unregister 后再刷新。
3. 仍旧：看是否 CDN/代理缓存；对一下响应头 `Cache-Control`。

### 3. 排障清单（可直接背）

**白屏**

1. Console：第一条红错是谁。
2. Network：主 JS/CSS 是否 404、是否拦了。
3. Elements：`#root` / `#app` 里有没有节点。

**接口挂 / 数据不对**

1. Network → Fetch/XHR → Status + Response。
2. 401→Token；CORS→OPTIONS/ACAO；500→后端。
3. Copy as cURL 对照；看 Initiator 是否重复请求。

**页面卡 / 输入延迟**

1. Performance 录制复现。
2. 看 Long Task + 火焰图最宽黄条。
3. Bottom-Up 按 Self；对源码改完再录对比。

**登录态诡异**

1. Application 看 Cookie 域名是否匹配（www vs 裸域）。
2. SameSite / Secure 是否导致跨站带不上。
3. 多 Tab 互相踢：看是否广播注销。

### 4. 和 AI 项目结合的一句

流式对话：Network 看 SSE 是否 pending、是否 canceled；卡顿时 Performance 看是否每 token 重渲染整棵消息树。

## 可能追问

- 为什么有的 Cookie 在 Application 看得到但 document.cookie 没有？→ HttpOnly，防 XSS 偷票。
- 清 LocalStorage 会不会影响 Cookie？→ 一般不会；Clear site data 可选范围更大。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [Cookie 三兄弟](../01-JavaScript/07-网络存储与安全/描述浏览器中 cookie、`sessionStorage` 和 `localStorage` 之间的区别.md)
- [水平/垂直越权](../13-前端安全/01-水平越权与垂直越权.md)
- [前端如何预防越权](../13-前端安全/02-前端如何预防越权.md)
- [实操：清 Token](14-实操-清Token复现未登录.md)
- [小程序登录与鉴权](../06-Taro小程序/小程序登录与鉴权.md)
