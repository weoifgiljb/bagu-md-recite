# 题 5：操作 DOM 怎样更不卡？

## 面试官可能怎么问

- 什么触发回流？
- DocumentFragment？
- 和框架性能优化的关系？

## 口述结构（90 秒）

1. 回流（reflow/layout）：几何/结构变，贵；重绘（repaint）：外观变，相对便宜
2. 忌：写-读-写穿插逼浏览器同步布局
3. 批量：fragment、合并 class、离线 DOM
4. 动画优先 `transform`/`opacity`；大列表虚拟化

## 参考答案

### 1. 什么触发回流（对应追问）

易回流：改宽高/位置/`display`、增删节点、改字体、读布局属性（`offsetHeight`、`getBoundingClientRect`）前若有脏样式等。  
相对偏重绘：改 `color`、`background`（不改几何）。

**坏步骤（强制同步布局）：**

```js
for (const el of list) {
  el.style.width = el.offsetWidth + 1 + 'px' // 读+写循环 = 多次 layout
}
```

**好步骤：**

```js
// 1) 先批量读
const widths = list.map((el) => el.offsetWidth)
// 2) 再批量写
list.forEach((el, i) => { el.style.width = widths[i] + 1 + 'px' })
// 或一次加 class，让 CSS 算
container.classList.add('compact')
```

### 2. DocumentFragment（对应追问）

把多次插入合成一次挂载：

```js
const frag = document.createDocumentFragment()
for (const item of items) {
  const li = document.createElement('li')
  li.textContent = item.title
  frag.append(li)
}
ul.append(frag) // 一次插入，减少中间回流
```

现代也可用一次性 `ul.innerHTML = safeHtml`（**仅当内容可信/已消毒**）或框架的列表渲染。

### 3. 和框架优化的关系

| 原生手段 | 框架对应 |
| --- | --- |
| 少操真实 DOM | 虚拟 DOM / 编译优化 / 细粒度更新（Vue3） |
| 批量插入 | 列表 key、一次状态提交 |
| 大列表 | 虚拟列表（只挂载可视区） |
| 动画 | GPU 友好属性；避免每帧改 layout |

业务例子：流式打字机——**按帧/按字符缓冲合并**再写 UI，不要每个 token 都强制 `offsetHeight` 测高度。

### 4. 实操清单（面试可背）

1. 能 CSS 解决的不要 JS 逐像素改  
2. 读写分离；缓存布局值  
3. 动画用 `transform`/`opacity`  
4. 列表超长上虚拟列表  
5. 用 Performance/Performance panel 验证，不空口

## 可能追问

- `requestAnimationFrame`？→ 跟刷新对齐改视觉，避免无意义中间帧。  
- `will-change`？→ 提示浏览器分层，滥用反而吃内存。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
