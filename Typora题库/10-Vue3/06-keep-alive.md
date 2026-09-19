# 题 6：keep-alive 原理是什么？缓存了什么？有哪些坑？

## 面试官可能怎么问

- keep-alive 缓存的是 DOM 还是组件实例？
- include / exclude / max 怎么用？LRU 是什么？
- 和路由、onActivated 怎么配合？有哪些常见坑？

## 口述结构（90 秒）

1. 缓存的是**组件实例（VNode/实例状态）**，切换时不销毁，只停用
2. 生命周期多一对：activated / deactivated（Composition：onActivated/onDeactivated）
3. include/exclude 按 name 匹配；max 超限按 LRU 淘汰
4. 路由场景：`<keep-alive><router-view/></keep-alive>` 或包裹具体页
5. 坑：无名组件、缓存不刷新、内存、监听器未在 deactivated 暂停

## 参考答案

### 1. 缓存的是什么？

`keep-alive` 是抽象组件：切走子组件时**不卸载实例**，把 VNode/实例放进缓存；切回时再挂上去，**data/setup 状态还在**（滚动位置、表单未提交内容、分页页码）。

- 不是简单「把 DOM 字符串存起来」；是**组件实例级缓存**。  
- 被缓存时走 `deactivated`，回来走 `activated`；**不会再走 mounted**（首次除外）。  
- 真正销毁（被 exclude、超 max 淘汰、外层销毁）才 `unmounted`。

```vue
<keep-alive :include="['UserList', 'OrderList']" :max="10">
  <component :is="current" />
</keep-alive>
```

### 2. include / exclude / max（LRU）

```vue
<script setup>
// 组件必须有 name（script setup 可用 defineOptions({ name: 'UserList' })）
</script>
```

| API | 作用 |
| --- | --- |
| `include` | 只有匹配的 name 才缓存（字符串/正则/数组） |
| `exclude` | 匹配的不缓存，优先级高于 include |
| `max` | 最多缓存几个；超出按 **LRU**：最久未访问的淘汰并真正销毁 |

步骤建议：

1. 给需要缓存的页面起稳定 `name`。  
2. 白名单 `include`，避免整站全缓存把内存打爆。  
3. 列表页设 `max`（如 5～10）；详情若带巨大富文本可 exclude。  
4. 需要「强制刷新缓存页」：改 `:key`、或从 include 临时移除、或在 `onActivated` 里按版本号拉数。

### 3. 路由配合与常见坑

```vue
<!-- App.vue 示意 -->
<router-view v-slot="{ Component }">
  <keep-alive :include="cachedViews">
    <component :is="Component" />
  </keep-alive>
</router-view>
```

```ts
// 页面内
onActivated(() => {
  // 每次露出：静默刷新未读数；恢复滚动可靠自身状态
  refreshSilent()
  startPolling()
})
onDeactivated(() => {
  stopPolling() // 关键：别在后台轮询
})
```

**坑与处理：**

1. **组件没 name** → include 失效，看起来「keep-alive 没用」。  
2. **以为每次进入都 mounted** → 首屏逻辑只写 mounted 会不跑；刷新类放 `onActivated`。  
3. **缓存了带 WS/定时器的页** → 必须在 deactivated 停，activated 再开。  
4. **同一组件多实例**（不同 id 详情）→ 只靠 name 会串缓存；给 `router-view` 或页根 `:key="route.fullPath"`，或不用 keep-alive 缓存详情。  
5. **内存** → DevTools Components 看实例是否堆积；max + 按路由 meta 维护 `cachedViews`。

**业务例子**：后台「用户列表 → 详情 → 返回」保留筛选与滚动；IM 会话列表缓存，会话详情按 id 用 key 区分或不缓存。

**验收**：返回列表筛选项仍在；切走后 Network 无轮询；include 外的页每次进入会重新 mounted。

## 可能追问

- 和 `v-if` 一起？→ 被 v-if 干掉会销毁，缓存没了。
- 缓存里能手动 prune？→ 维护 include 数组或升 key。
- SSR？→ keep-alive 主要客户端；需注意水合策略。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
