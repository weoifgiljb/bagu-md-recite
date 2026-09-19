# 题 2：Elements 和 Console 日常怎么排查样式和报错？

## 面试官可能怎么问

- 样式明明写了不生效，你怎么查？
- `$0` 是什么？条件断点呢？
- 怎么模拟 :hover / 暗色主题？

## 口述结构（90 秒）

1. Elements：选中 → Styles → Computed → 盒模型
2. 被划掉的样式 = 被覆盖；看来源文件行号
3. Console：读堆栈、`$0`、临时改数据验证
4. 流程：先确认「选没选对节点」，再谈优先级

## 参考答案

### 1. Elements 实操路径

1. Ctrl+Shift+C 点中页面元素，或在 DOM 树里搜 class。
2. 右侧 **Styles**：看匹配到的规则；**划掉** = 被更高优先级/后加载规则覆盖。
3. 点开规则右侧文件名：跳到 Sources 里对应 CSS。
4. **Computed**：最终算出来的值（含继承）；下面有盒模型图（content / padding / border / margin）。
5. 右侧 **+** 或点 element.style 可临时改样式，验证「是不是 CSS 问题」而不改代码。

强制伪类：选中节点 → Styles 面板 **:hov** → 勾选 `:hover` / `:focus`，不用真的把鼠标悬上去。

### 2. 样式不生效排查清单（步骤）

1. **是不是选错节点**（组件库常包一层）。
2. **类名有没有挂上**（Vue/React 条件 class）。
3. **是否被覆盖**：看划线；算 specificity；有没有 `!important`。
4. **是否被缩短/未加载**：Network 里 CSS 是否 200；Scoped CSS / CSS Modules 哈希类名是否匹配。
5. **盒模型误解**：`width` + `padding` 在 `content-box` 下会撑破布局；看 Computed 实际宽高。

### 3. Console 常用

- 红色报错：点开堆栈，从 **你的业务文件** 那一行看起（先忽略 node_modules 里的噪声）。
- **`$0`**：当前 Elements 里选中的 DOM 节点；`$1` 是上一次选中的。
- `copy($0)` / `copy(object)`：把对象拷到剪贴板。
- `console.table(arr)`：表格看数组。
- Filter 框可滤 `error` / 自己的关键字。

临时验证：

```js
$0.style.outline = '2px solid red'
document.querySelector('.chat-list')?.scrollHeight
```

### 4. Sources 里和 Console 配合

- 在行号处打断点；右键 **Add conditional breakpoint**，例如 `item.id === 'xxx'`，少暂停。
- **Pretty print** `{ }`：压缩后的包可读一些。
- 断住后看 Scope / Call Stack，在 Console 里可以直接访问当前作用域变量。

## 可能追问

- 为什么 Computed 和 Styles 里写的不一致？→ Styles 是「声明」，Computed 是「算完」；还有继承、初始值。
- 如何看事件绑在谁身上？→ Elements → 选中节点 → 右侧 Event Listeners（注意祖先委托）。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [回流重绘与 DOM 性能](../12-BOM-DOM-Ajax/05-回流重绘与DOM性能.md)
- [CSS 选择器性能](../11-CSS与样式/30-CSS选择器性能.md)
- [层叠上下文 z-index](../11-CSS与样式/12-层叠上下文z-index.md)
- [实操：查样式覆盖](11-实操-查样式被谁覆盖.md)
