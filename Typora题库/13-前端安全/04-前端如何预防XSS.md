# 题 4：从前端角度如何预防 XSS？

## 面试官可能怎么问

- Vue/React 默认安全吗？
- 什么时候会翻车？
- 你会采取哪些具体手段？

## 口述结构（90 秒）

1. 框架默认文本插值会转义，相对安全
2. 翻车点：`v-html`、`dangerouslySetInnerHTML`、富文本、拼接 href/js
3. 手段：不信任输入、消毒、CSP、HttpOnly、避免危险 API
4. 流程：渲染管道默认安全，例外走白名单

## 参考答案

### 1. Vue/React 默认安全吗？

**默认文本插值相对安全**（会转义成文本节点），但不是「整个项目免疫」。  
Vue：`{{ msg }}` 安全；`v-html` 危险。  
React：`{msg}` 安全；`dangerouslySetInnerHTML` 危险。

### 2. 什么时候会翻车（清单）

1. 为了渲染富文本直接 `v-html=用户内容`  
2. 用字符串拼 `<script>` 或 `javascript:` 链接  
3. 把不可信数据塞进 `eval`、`new Function`、`setTimeout(字符串)`  
4. 服务端返回 HTML 片段原样进页面  
5. Markdown/公式插件默认放开 HTML  

### 3. 具体手段（步骤）

1. **默认当文本**：能用 `textContent` / 框架文本插值就不要 HTML  
2. **必须 HTML**：用经过维护的 sanitizer（如 DOMPurify）白名单标签/属性  
3. **链接**：校验协议，只允许 `http:`/`https:`/`mailto:`，拒绝 `javascript:`  
4. **CSP**：限制脚本来源，降低内联脚本杀伤（见题 6）  
5. **Cookie**：会话 Cookie `HttpOnly; Secure; SameSite`  
6. **Code Review**：搜 `v-html` / `innerHTML` / `dangerouslySetInnerHTML`  

```js
import DOMPurify from 'dompurify'
el.innerHTML = DOMPurify.sanitize(html, { USE_PROFILES: { html: true } })
```

业务例子：AI Markdown 渲染必须进消毒管道；普通气泡内容走文本/安全渲染器。


### 4. 上线前检查（可执行）

1. 全仓搜危险 API 与 `v-html`  
2. 对用户生成内容页做一次「恶意 payload」回归（脚本、svg onload、markdown 图片）  
3. 确认响应头 CSP 在预发已开启 report-only 或 enforce  
4. 确认 token 存储方案与 XSS 风险被产品接受或已改为 HttpOnly 会话  

## 可能追问

- 消毒就万无一失吗？→ 配置错误、浏览器解析差异仍可能漏；要叠加 CSP。  
- 为什么禁止 `javascript:` URL？→ 点击即执行脚本。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
