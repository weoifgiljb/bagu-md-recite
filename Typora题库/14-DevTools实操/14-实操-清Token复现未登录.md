# 题 14：实操——清 Token/Cookie 复现未登录，并核对 401

## 面试官可能怎么问

- 怎么本地稳定复现「登录过期」？
- 401 之后前端该有什么行为？你如何验证？
- HttpOnly Cookie 和 localStorage Token 排查差在哪？

## 口述结构（90 秒）

1. Application 找到 Token 存哪
2. 清掉或改坏再操作需鉴权接口
3. Network 确认 401 与是否跳转登录
4. 说明 Cookie HttpOnly 只能在 Application 删

## 参考答案

### 操作步骤（照着点）

1. 先 **正常登录** 进入业务页。
2. F12 → **Application**（旧版可能叫 Storage）。
3. 左侧依次看：
   - **Local Storage** / **Session Storage**：有没有 `token`、`access_token`
   - **Cookies**：选中你的站点域名，看会话 Cookie
4. 复现未登录（选一种）：
   - 删掉 Local Storage 里的 token 键
   - 或把 token 值改成 `a.b.c` 乱写
   - 或选中 Cookie → Delete（HttpOnly 也只能在这里删）
5. 回到页面，触发一个 **需要登录** 的操作（刷新、点个人中心、发消息）。
6. **Network → Fetch/XHR** 看是否出现 **401/403**：
   - 有 401 + 跳转登录页 = 拦截器/路由守卫正常
   - 有 401 但页面假数据/白屏 = 前端没处理错误分支
   - 没有 401 仍进页 = 路由没守住或接口其实没鉴权
7. （可选）Application 左侧 **Clear site data** 一键清空（更狠，注意别清错环境）。

### 口述要点

- Token 在 localStorage：XSS 可被偷，要配合 CSP/消毒；过期用 401 统一踢出。
- Cookie HttpOnly：JS 读不到，排查必须看 Application；跨站还要看 SameSite。

## 可能追问

- 多 Tab 退出如何同步？→ `storage` 事件或广播频道，面试提到即可。
- 清了 Storage 但 Cookie 还在？→ 两套凭证要一起看，别只清一边。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [Application 排查清单](08-Application与排查清单.md)
- [AI 功能鉴权](../03-AI前端/AI功能鉴权.md)
- [小程序登录与鉴权](../06-Taro小程序/小程序登录与鉴权.md)
- [CSRF 与 Cookie](../13-前端安全/07-CSRF与Cookie.md)
- [越权预防](../13-前端安全/02-前端如何预防越权.md)
