# 题 11：模型/助手输出的 XSS 与富文本消毒？

## 面试官可能怎么问

- 模型输出能直接 innerHTML 吗？
- DOMPurify、链接协议白名单怎么做？
- 小程序里没有 DOM，怎么消毒？可怎么提 tintRichHtml？

## 先自己答（90 秒）

## 参考答

**原则**：模型输出 = **不可信内容**（可能含 prompt 注入带来的恶意 HTML/脚本，或被投毒文档污染）。

**Web（Vue/React）**
- 禁止直接 `v-html` / `dangerouslySetInnerHTML` 原始字符串
- Markdown → HTML 后走 **DOMPurify**（或等价）：白名单标签/属性
- 链接：只允许 `http:` / `https:` / `mailto:`；拒绝 `javascript:`、`data:` 可执行类型
- 图片：限制协议与可选域名；注意 `onerror` 等事件属性必须剥掉

**打字机/流式**
- 流式过程中半截 HTML 更危险也更易破版；可先纯文本，结束再消毒渲染
- 代码块用文本节点展示，不要当 HTML 解析

**小程序 / Taro**
- 无浏览器 DOMPurify 时：服务端先消毒，或自研受限子集（允许的标签着色，如 `tintRichHtml`：只做高亮/着色转换，不执行脚本）
- `rich-text` 组件也有标签限制，仍按白名单思维

**业务例子**：助手把文档 HTML 片段塞进回复——必须消毒后再进 ChatWidgets；审阅页展示 Doc 富文本同样处理。

## 可能追问

- Markdown 里的 HTML 开关键？→ 默认关或强消毒。
- CSP 能替代消毒吗？→ 互补，不能只靠 CSP。

## 我的四行

- 定义：
- 原理：
- 业务例子：
- 可能追问：
