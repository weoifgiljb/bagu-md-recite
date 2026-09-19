# 题 5：Performance 面板怎么录制？和 Lighthouse 有什么区别？

## 面试官可能怎么问

- 怎么录一段卡顿？录之前要准备什么？
- Summary 里 Scripting / Rendering / Painting 什么意思？
- 什么时候用 Performance，什么时候用 Lighthouse？

## 口述结构（90 秒）

1. 用途：还原「那段时间」主线程在干什么
2. 录制步骤：清缓存设定 → 录 → 复现 → 停
3. 先看 FPS/CPU 总览，再进 Main 火焰图
4. Lighthouse 是跑分建议；Performance 是你操作的时间线

## 参考答案

### 1. 录制前准备

1. 关闭无关标签，减少噪声。
2. Network 勾 **Disable cache**；需要可 CPU **4× slowdown**、网络 Fast 3G（放大问题）。
3. Performance 里勾选 **Screenshots**（可选，便于对齐画面）。
4. 想看首次加载：用面板上的 **刷新图标开录**；想看交互卡顿：先点 Record 再操作。

### 2. 标准步骤（交互卡顿）

1. 打开 Performance。
2. 点圆点 **Record**（或 Ctrl+E）。
3. 立刻复现：滚动列表、打开弹窗、打字、切 Tab 等。
4. 再点 Stop。控制在 **几秒到十几秒**，太长难读。
5. 先看上方 **FPS**（红=掉帧）、**CPU** 饱和段、**NET**。
6. 再看 **Main** 轨道火焰图；下方 Summary 看时间花在哪一类。

### 3. Summary 颜色大类

- **Scripting（黄）**：JS 执行、框架 diff、JSON.parse 等。
- **Rendering（紫）**：Style、Layout（重排）。
- **Painting（绿）**：绘制、合成相关。
- **Loading**：解析 HTML/CSS、部分加载工作。
- **Idle**：空闲。

卡顿时若 Scripting 占比极高：先查大循环、同步大计算、过重的列表渲染。若 Rendering 高：查频繁布局、复杂 CSS。

### 4. Performance vs Lighthouse

| | Performance | Lighthouse |
|--|-------------|------------|
| 数据来源 | 你录的那一段真实操作 | 工具按流程加载页面打分 |
| 擅长 | 卡顿、长任务、火焰图定位函数 | FCP/LCP/CLS 等指标与改进建议 |
| 用法 | 复现 → 录 → 分析 | 跑一次看报告 |

面试说法：性能「定位到函数」用 Performance；「首页指标与清单」用 Lighthouse（或 Web Vitals）。

### 5. 常见录制失败

- 录太长：先用滚轮缩放时间轴，框选卡顿那一小段。
- 没复现到：边录边操作，确认 FPS 红条出现过。
- 生产包无 source map：函数名都是 a、b；本地/预发开 source map 更好查。

## 可能追问

- 为什么要 CPU 4×？→ 高端机不明显的卡，降速后更容易在火焰图里暴露。
- 主线程和下线轨道？→ 还有 GPU、Network、Frames；主卡顿优先看 Main。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [火焰图怎么读](06-火焰图怎么读.md)
- [JS 性能瓶颈](../01-JavaScript/12-性能优化/JavaScript 应用程序中常见的一些性能瓶颈是什么？.md)
- [性能衡量工具](../01-JavaScript/12-性能优化/有哪些可以用来衡量和分析 JavaScript 性能的工具？.md)
- [Vue3 性能优化](../10-Vue3/10-Vue3性能优化.md)
