# 题 1：什么是 BOM？常见对象有哪些？

## 面试官可能怎么问

- BOM 和 DOM 区别？
- window 上都有什么？
- 说一下 navigator / screen / location / history

## 口述结构（90 秒）

1. BOM：浏览器对象模型，JS 操作「窗口与浏览器能力」
2. 入口是 `window`；DOM 的 `document` 也挂在上面
3. 常考四件套：location / history / navigator / screen
4. 边界：BOM 管壳，DOM 管页

## 参考答案

### 1. BOM 和 DOM 区别（先答清边界）

BOM（Browser Object Model）描述浏览器窗口相关对象；DOM（Document Object Model）描述页面文档树。面试官要听你**会不会把「跳转页面」和「改某个 div 文字」说成一类东西**。

对比开口：  
- 改地址栏、前进后退、读 UA、看是否在线 → **BOM**  
- 查节点、改文本、绑点击、插列表项 → **DOM**  
- 两者在浏览器里通过 `window.document` 连在一起，但职责不同

### 2. window 上都有什么（按清单背）

把 window 想成「浏览器给的工具箱」，分类记：

1. **导航类**：`location`、`history`  
2. **环境类**：`navigator`、`screen`、`devicePixelRatio`  
3. **定时与帧**：`setTimeout`、`setInterval`、`requestAnimationFrame`  
4. **窗口尺寸**：`innerWidth` / `innerHeight`（注意乱读会逼布局计算）  
5. **文档入口**：`document`（进入 DOM 世界）

落地步骤（检查离线再请求）：  
1. 读 `navigator.onLine` 或监听 `window` 的 `online`/`offline`  
2. 离线则提示并禁止提交  
3. 恢复在线后重试队列

### 3. navigator / screen / location / history 怎么讲

**location（当前 URL）**  
字段：`href`、`pathname`、`search`、`hash`、`origin`。  
方法：`assign`（可后退）、`replace`（替换历史，登录成功跳转常用）、`reload`。  
步骤：用 `URLSearchParams(location.search)` 取 `docId`，再请求详情。

**history（会话历史）**  
`back`/`forward`/`go`；HTML5 的 `pushState`/`replaceState` 让 SPA 改 URL 却不整页刷新。  
步骤：路由库调用 `pushState` → 用户点后退触发 `popstate` → 应用按 URL 重新渲染。

**navigator（运行环境）**  
`userAgent`、`language`、`onLine`；能力探测前先判断 API 是否存在。不要只靠 UA 字符串判移动端。

**screen（屏幕）**  
物理屏宽高；响应式布局优先用 CSS 媒体查询，而不是到处读 `screen.width`。

### 4. 业务例子

SaleSmartly / AI 站：登录后 `location.replace` 进工作台；列表筛选条件进 URL query；真正页面跳转交给 Vue Router，但你要能下沉讲到 BOM。

## 可能追问

- iframe 里 window？→ 每个 frame 一份，跨域读写受限。  
- 严格模式 / ES Module 顶层 this？→ 不一定等于 window。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
