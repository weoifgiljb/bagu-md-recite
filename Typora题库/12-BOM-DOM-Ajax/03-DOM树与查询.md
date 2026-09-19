# 题 3：DOM 是什么？怎么查改节点？

## 面试官可能怎么问

- HTMLCollection 和 NodeList 区别？
- querySelector 和 getElementById？
- 虚拟 DOM 和真实 DOM 关系？

## 口述结构（90 秒）

1. DOM：HTML 解析成的树，JS 可查询/增删改节点
2. 查：id / 选择器 / 标签名集合；改：创建、插入、属性、文本
3. 集合有 live / static 差异，面试爱问
4. 框架：先在虚拟 DOM 上算 diff，再批量打补丁到真实 DOM

## 参考答案

### 1. DOM 是什么（定义 + 操作闭环）

浏览器把 HTML 建成文档树。常见步骤：

1. **查**：拿到节点引用  
2. **改**：改文本/属性/子树  
3. **插/删**：`append` / `remove` / `replaceWith`  
4. **听事件**：`addEventListener`（见题 4）

```js
const el = document.querySelector('.item')
el.textContent = 'safe text'          // 优先：无 HTML 解析，防 XSS
el.setAttribute('data-id', '1')
el.dataset.id                         // 等同读 data-id
const li = document.createElement('li')
li.textContent = 'new'
document.querySelector('ul').append(li)
```

**别默认 `innerHTML = userInput`**——有 XSS；必须消毒或改用文本 API。

### 2. HTMLCollection vs NodeList（对应追问）

| | HTMLCollection | NodeList |
| --- | --- | --- |
| 常见来源 | `getElementsByTagName` / `children` | `querySelectorAll` / `childNodes` |
| 是否 live | 多数 **live**（DOM 变，集合跟着变） | `querySelectorAll` 结果通常 **static** |
| 遍历 | 类数组；现代可 `Array.from` | 同上；有的实现带 `forEach` |

```js
const live = document.getElementsByClassName('x') // HTMLCollection, live
const staticList = document.querySelectorAll('.x') // NodeList, static 快照
```

开口：**先说 live/static，再说别在遍历 live 集合时边删边加节点，易翻车。**

### 3. querySelector vs getElementById

| API | 特点 | 何时用 |
| --- | --- | --- |
| `getElementById('a')` | 最快路径之一，只认 id | 页面唯一锚点、性能敏感老代码 |
| `querySelector('.a #b')` | CSS 选择器，灵活 | 组件根内查找、复杂选择 |
| `querySelectorAll` | 全匹配静态列表 | 批量操作前先转数组 |

步骤建议：  
1. 有稳定 id → `getElementById`  
2. 需要「当前组件根下」→ `root.querySelector`（别每次从 `document` 扫全树）  
3. 要改很多节点 → 一次查出，再循环，避免循环里重复 query

### 4. 虚拟 DOM vs 真实 DOM

- **真实 DOM**：浏览器渲染要用的节点，改它贵（易回流/重绘）  
- **虚拟 DOM**：用 JS 对象描述 UI；更新时 diff 出最小补丁，再应用到真实 DOM  
- Vue3：编译 + 响应式依赖收集，不是「每次整树傻 diff」；但面试仍要会说 **VNode → patch → 真实 DOM**

业务例子：AI 对话列表用框架声明式更新；只有富文本预览等少数场景才手写 `innerHTML`（且必须 sanitize）。

## 可能追问

- `childNodes` vs `children`？→ 前者含文本/注释；后者仅元素。  
- Shadow DOM？→ 封装内部树与样式，Web Component 常用。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
