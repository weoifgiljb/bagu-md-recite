# 题 5：nextTick 是做什么的？什么时候必须用？

## 面试官可能怎么问

- 改了数据为什么马上读 DOM 还是旧的？
- nextTick 和 setTimeout(fn,0) 有什么区别？
- 有哪些场景必须 nextTick？能不用吗？

## 口述结构（90 秒）

1. Vue 异步批量更新：同一事件循环里多次改状态，只排队一次 DOM 更新
2. nextTick：等当前队列里的 DOM 更新完成后再跑回调
3. 实现上优先微任务（Promise.then）；与宏任务 setTimeout 时机不同
4. 典型场景：改 v-if 后 focus、拿更新后 scrollHeight、打字机滚到底
5. 能用 watch flush:post / 模板 ref+onMounted 就少堆 nextTick

## 参考答案

### 1. 为什么读 DOM 还是旧的？

```ts
count.value++
console.log(document.querySelector('.n')?.textContent) // 仍可能是旧值
await nextTick()
console.log(document.querySelector('.n')?.textContent) // 新值
```

原因：Vue3 把组件更新丢进**队列**，在当前同步代码结束后再 flush。好处是：一次点击里改 10 个 ref，只渲染一次。所以「改数据 → 立刻量 DOM」中间隔着一次更新；要用 `nextTick`（或 `flush:'post'` 的 watch）等更新结束。

### 2. nextTick vs setTimeout(0)

| | nextTick | setTimeout(fn, 0) |
| --- | --- | --- |
| 队列 | 通常微任务（Promise） | 宏任务 |
| 与 Vue 更新关系 | **专门等 Vue 的 DOM 更新队列** | 只保证「稍后」，不保证排在 Vue flush 之后（多数情况碰巧可以，但不契约） |
| 嵌套更新 | 可在同一轮更新逻辑里继续 await nextTick | 多一层事件循环，易闪烁/抖动 |

源码直觉：调度器 `queueJob` → flush → 再跑 `nextTick` 回调。面试说「nextTick 跟的是 Vue 的更新，不是随便延后一下」即可。

```ts
import { nextTick, ref } from 'vue'
const show = ref(false)
const input = ref<HTMLInputElement | null>(null)

async function open() {
  show.value = true          // v-if 为真，但本同步栈内 input 仍可能是 null
  await nextTick()
  input.value?.focus()       // 此时子节点已挂上
}
```

### 3. 必须用 / 可以不用的场景

**常用必须：**

1. `v-if`/`v-show` 切换后对输入框 `focus()`、对弹层量宽高。  
2. 列表渲染后读 `scrollHeight`，滚到最底（聊天、日志）。  
3. 改 class 后强制读 layout（少用；注意强制同步布局性能）。  

**步骤（聊天滚底）：**

```ts
async function pushMsg(m) {
  messages.value.push(m)
  await nextTick()
  const box = listRef.value
  if (box) box.scrollTop = box.scrollHeight
}
```

**可以少用：**

- 只用到「数据变了做副作用」→ `watch(..., { flush: 'post' })`。  
- 仅首次挂载读 DOM → `onMounted`。  
- 不依赖 DOM 的逻辑 → 直接写，别套 nextTick 显得「玄学」。

**业务例子**：流式 Markdown 追加后 `await nextTick()` 再滚底；Tab 切到编辑器再 `focus`；表格列宽根据表头文字测量。

**验收**：去掉 nextTick 会 focus 失败或 scrollTop 不准；加上后一次更新只滚一次，无「先错位再跳」。

再对比调度：同一事件里 `a.value=1; b.value=2` 只会排队一次渲染；`nextTick` 回调里如果再改依赖，会进入**下一轮**更新队列，因此可能再次 await。调试时在回调打 log 看 DOM 文本，比空谈微任务更有说服力。若只是「数据变了拉接口」，优先 `watch`，把 nextTick 留给真正的 DOM 读取/聚焦/滚动。

## 可能追问

- 连续 await nextTick 两次？→ 一般一次够；二次多为等子组件再渲染。
- 和 `requestAnimationFrame`？→ 跟绘制帧；量动画中间态用 rAF，等 Vue DOM 用 nextTick。
- 更新队列报错？→ 回调里继续改状态会再排队，注意死循环。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
