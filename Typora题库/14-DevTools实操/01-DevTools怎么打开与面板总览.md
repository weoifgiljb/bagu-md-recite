# 题 1：Chrome DevTools 怎么打开？各面板分别干什么？

## 面试官可能怎么问

- 平时怎么打开 DevTools？命令菜单有什么用？
- Elements / Network / Performance / Application 分别什么时候用？
- Dock 到右边和独立窗口怎么选？

## 口述结构（90 秒）

1. 打开方式：F12、右键检查、Ctrl+Shift+I
2. 命令菜单 Ctrl+Shift+P 搜面板/功能
3. 六大面板各一句话 + 典型场景
4. 调试习惯：先复现，再开对的面板，别一上来乱点

## 参考答案

### 1. 怎么打开

1. **F12**（Windows/Linux）或 **Cmd+Option+I**（Mac）。
2. 页面空白处 **右键 → 检查**（会顺带选中该元素）。
3. 菜单：更多工具 → 开发者工具。
4. **Ctrl+Shift+C**：进入「检查元素」模式，鼠标点哪看哪。

Dock：DevTools 右上角三个点 → Dock side。页面宽就 **右边/下边**；要看完整布局或双屏就 **独立窗口**。

### 2. 命令菜单（必会）

**Ctrl+Shift+P**（Mac：Cmd+Shift+P）打开 Command Menu，可搜：

- Show Network / Show Performance
- Disable JavaScript（临时关 JS 看裸 HTML）
- Capture full size screenshot
- 切 Dark mode 等

记不住图标时，用命令菜单最快。

### 3. 面板一句话 + 何时用

| 面板 | 干什么 | 典型场景 |
|------|--------|----------|
| **Elements** | DOM + CSS | 样式不对、看盒模型、强制 :hover |
| **Console** | 日志、报错、临时跑 JS | 红错、打 `$0`、验证变量 |
| **Sources** | 断点、调用栈 | 跟函数、条件断点、pretty print |
| **Network** | 请求瀑布、Headers/Body | 接口失败、慢、CORS、SSE |
| **Performance** | 录一段再分析 | 卡顿、掉帧、长任务、火焰图 |
| **Application** | 存储、Cookie、SW | Token、清缓存、Service Worker |
| **Lighthouse** | 跑分报告 | 首屏/SEO 体检（偏报告，不替代表现录制） |

### 4. 实操顺序（白屏 / 卡 / 接口挂）

1. **白屏**：先 Console 看红错 → Elements 看根节点是否挂上 → Network 看 JS/CSS 是否 404。
2. **卡顿**：Performance 录制复现 → 看 Main 火焰图。
3. **接口问题**：Network 过滤 Fetch/XHR → 点开 Status / Response。

### 5. 小提示

- 勾选 **Preserve log**（Network）再跳转，避免导航清空列表。
- 本地调试可勾 **Disable cache**（仅 DevTools 打开时生效）。
- 远程真机：`chrome://inspect` 或边栏 Devices（了解即可）。

## 可能追问

- Lighthouse 和 Performance 区别？→ 前者是审计报告，后者是你操作过程的时间线。
- 为什么 Disable cache 只在开着 DevTools 时有效？→ 这是 DevTools 的网络拦截选项，关掉工具就恢复浏览器默认缓存策略。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [日常排查跳转地图](00-日常排查跳转地图.md)
- [JS：调试工具](../01-JavaScript/11-测试与工程化/你使用什么工具和技术来调试 JavaScript 代码？.md)
- [React：如何调试](../02-React/09-其他/如何调试 React 应用程序？.md)
- [JS：性能衡量工具](../01-JavaScript/12-性能优化/有哪些可以用来衡量和分析 JavaScript 性能的工具？.md)
