# 题 5：富文本 / Markdown 场景怎么防 XSS？

## 面试官可能怎么问

- Markdown 转 HTML 安全吗？
- 图片、链接、表格有什么坑？
- AI 输出怎么渲染更稳？

## 口述结构（90 秒）

1. Markdown→HTML 默认不等于安全
2. 链接/图片/原始 HTML 是重灾区
3. 管道：解析 → 消毒 → 再渲染
4. AI 输出按「不可信用户内容」同级处理

## 参考答案

### 1. Markdown 转 HTML 安全吗？

**不安全（默认）。** 许多解析器允许原始 HTML，或生成可执行属性。  
步骤必须是：

1. Markdown parse → HTML AST/字符串  
2. **Sanitizer 白名单**（标签、属性、协议）  
3. 再进入 `v-html` / 安全渲染组件  
4. 能纯文本展示的控件不要走 HTML

```js
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'
const md = new MarkdownIt({ html: false, linkify: true }) // 先关 raw HTML
const dirty = md.render(src)
const clean = DOMPurify.sanitize(dirty, {
  ALLOWED_TAGS: ['p','br','strong','em','ul','ol','li','code','pre','a','img','table','thead','tbody','tr','th','td'],
  ALLOWED_ATTR: ['href','src','alt','title'],
  ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i,
})
```

### 2. 图片、链接、表格坑点

- **链接**：`javascript:`、`data:text/html` 点击执行  
- **图片**：`onerror` 事件；或超大图/跟踪像素  
- **表格/样式**：`style` 表达式、表达式注入（老 IE）；现代主要防属性  
- **SVG/Math**：若放开，攻击面显著变大——默认别允许  

步骤：链接只留 http(s)/mailto；图片只 http(s)；去掉事件属性与 `style`（除非极严白名单）。

### 3. AI 输出怎么更稳

把模型输出当成**不可信用户内容**：  
1. 同样走 Markdown + sanitize  
2. 代码块用高亮组件，不要 `innerHTML` 整块塞  
3. 「引用文档」只展示文本/只读卡片，不执行文档内脚本  
4. 需要交互的按钮是你自己的组件，不由模型 HTML 生成  

业务例子：打字机渲染只追加消毒后的安全 HTML，或增量更新文本节点。

## 可能追问

- 为什么 `html: false` 还要 DOMPurify？→ linkify/插件仍可能产出危险属性。  
- 公式/mermaid？→ 独立沙箱或服务端渲染，慎直接进页面。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
