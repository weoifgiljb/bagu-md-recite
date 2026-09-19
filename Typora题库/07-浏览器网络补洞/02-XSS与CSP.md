# 题 2：XSS 有哪些类型？前端怎么防？CSP 起什么作用？

## 面试官可能怎么问

- 反射型 / 存储型 / DOM 型怎么区分？
- 富文本、Markdown、AI 回复为何高危？
- CSP 能替代消毒吗？

## 口述结构（90 秒）

1. XSS：把脚本注入到受害者浏览器执行
2. 分类按「恶意脚本从哪来、怎么进页面」
3. 防：默认文本节点、消毒、HttpOnly、CSP
4. AI/Markdown 当不可信输入，白名单渲染

## 参考答案

### 1. 三类 XSS（步骤 + 例子）

1. **反射型**：恶意脚本在 URL/参数里，服务端立刻映入 HTML 返回。步骤：诱导点击链接 → 服务器回显 → 浏览器执行。  
2. **存储型**：脚本存进 DB（评论、简介），他人打开页面时加载执行。危害大、传播广。  
3. **DOM 型**：不经过服务端拼接，前端用 `innerHTML` / 危险 API 把位置哈希等写进 DOM。  

```js
// 危险
el.innerHTML = userInput
// 相对安全
el.textContent = userInput
```

### 2. 前端防护清单

1. **默认当文本**：React/Vue 文本插值默认转义；避免 `v-html` / `dangerouslySetInnerHTML` 喂裸数据。  
2. **必须富文本**：DOMPurify 等白名单消毒；禁止 `script`、`onerror`、`javascript:` URL。  
3. **Markdown**：先渲染再消毒，或用仅支持安全子集的渲染器。  
4. **Cookie**：会话 `HttpOnly` + `Secure`，降低偷 Cookie 价值。  
5. **CSP**：`Content-Security-Policy` 限制脚本源，`script-src 'self'`；尽量避免 `unsafe-inline`。  
6. **AI 回复**：模型输出当攻击者输入；引用链接校验协议。

### 3. CSP 与消毒关系

CSP 是**纵深防御**：即使漏了注入，也可能拦外域脚本或内联脚本。  
不能替代消毒：`javascript:` 链接、允许的内联事件、合法源上的 DOM 型仍可能出问题。  
落地步骤：先 Report-Only 收报告 → 收紧策略 → 再 enforce。

**业务例子**：AI 对话 Markdown 渲染前消毒；匹配文档标题用文本节点；管理端富文本必走白名单。

### 4. 快速自查（面试可举例）

1. 全局搜 `innerHTML` / `v-html` / `dangerouslySetInnerHTML` / `document.write`。  
2. 用户生成内容、AI 输出、URL query 是否进了 HTML。  
3. 第三方脚本是否可收束到 CSP nonce/hash。  
4. 管理端与 C 端是否同一套消毒（管理端常被忽视）。  
5. 报告通道：CSP report-uri / 错误监控里是否有 `script-src` 违规。  

一句话收口：**转义是默认，消毒是例外，CSP 是保险，HttpOnly 减损。**

## 可能追问

- mXSS？→ 浏览器解析差异导致消毒后再解析变危险，需成熟库与测试。
- Json 进 HTML？→ 别把 JSON 直接塞 script 标签；用安全序列化。
- 小程序 XSS？→ 无浏览器 DOM 模型，但仍有 web-view、富文本组件风险。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
