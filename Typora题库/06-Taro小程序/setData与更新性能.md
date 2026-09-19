# 题 1：小程序 setData 做了什么？为什么会卡？怎么优化？

## 面试官可能怎么问

- setData 的数据路径是什么？和直接改 this.data 有啥区别？
- 流式/打字机每字 setData 会怎样？
- 列表很长时怎么更新更稳？

## 口述结构（90 秒）

1. setData 不是改内存就完事，要序列化后经逻辑层→视图层通信
2. 频繁/大包 setData 会阻塞渲染，假打字机最容易踩
3. 优化：合并节流、路径更新、裁剪字段、分页/只保留可视区
4. 验收：真机看掉帧与 setData 耗时，不以开发者工具为准

## 参考答案

### 1. setData 做了什么（步骤）

1. 逻辑层（JS）调用 `this.setData(patch)` 或 Taro/React 运行时最终落到同类通信。  
2. 框架把 patch **序列化**（JSON 风格），经 **JSBridge / 双线程通信** 送到视图层。  
3. 视图层合并到渲染数据，触发 WXML/小程序组件树更新与重绘。  
4. 回调 `setData` 的 complete 在通信与合并完成后触发——**不等于**「下一帧已经画完」。

直接改 `this.data.xxx = 1` **不会**驱动视图；必须走 setData（或框架封装）。Taro React 里 `setState` / hooks 更新，编译到小程序端仍会变成有节制的 setData。

```js
// 原生思路：路径更新，避免整树替换
this.setData({
  'messages[3].content': nextText,
  'messages[3].status': 'streaming'
})
```

### 2. 为什么会卡（面试口径）

- **通信成本**：patch 越大、越频繁，序列化与跨线程开销越高。  
- **渲染成本**：视图层 diff/重排；长列表每次全量刷新更惨。  
- **主线程争用**：逻辑层还在算 Markdown/匹配时又狂 setData，体感卡顿。  
- AI 假打字机若「每字一次 setData」，等于把通信打满——开发者工具可能还行，**真机必现**。

### 3. 优化清单（按优先级）

1. **合并更新**：50–100ms 节流/raf 合并；流式只改「当前气泡」字段。  
2. **路径 setData**：`'list[i].x'`，不要每次 `setData({ list: 全新大数组 })`（除非必须）。  
3. **裁剪 payload**：视图不需要的大字段（原文、embedding、调试信息）不要放 data。  
4. **列表策略**：分页、只保留最近 N 条在视图；更长用虚拟列表或「点击加载更早」。  
5. **计算下放**：重计算在逻辑层做完再一次 setData；避免在 `observers` 里连环 setData。  
6. **分包与包体**：Markdown/高亮别全进主包，减少启动与内存压力间接改善卡顿。

```ts
// 伪代码：流式缓冲
let buf = ''
let timer: any
function onChunk(s: string) {
  buf += s
  if (timer) return
  timer = setTimeout(() => {
    timer = null
    const text = buf
    setDataPath(`messages[${idx}].content`, text)
  }, 80)
}
```

**业务例子（doc-review-taro / AI Tab）**：助手回复流式或假打字机时，只更新当前 message 的 `content/status`；匹配文档 `matches` 等完整结果一次到位，不跟每个字符绑定。

**验收**：微信开发者工具 Performance / 真机体验分析里看 setData 耗时；快速输入与长回复时帧率不塌。

## 可能追问

- setData 有大小上限吗？→ 有实践上限（常见讨论约 1MB 量级），超大包会失败或极慢，应拆分。
- Taro React 还要手写路径 setData 吗？→ 优先让框架批更新；热点路径可降频或局部 state。
- 和 Vue nextTick 类比？→ 都是「改完别立刻假设 DOM 已好」，但小程序多了跨线程序列化这层。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
