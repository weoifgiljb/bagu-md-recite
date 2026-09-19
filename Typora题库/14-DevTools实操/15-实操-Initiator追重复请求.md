# 题 15：实操——同一接口打了两次，用 Initiator 追到源码

## 面试官可能怎么问

- 列表接口为何会 double fetch？
- 你怎么从 Network 跳回发请求的那行代码？
- React StrictMode 和业务重复请求怎么区分？

## 口述结构（90 秒）

1. Network 里按 Name 排序，找成对相同请求
2. 点 Initiator 看文件:行号
3. 对照 useEffect 依赖、StrictMode、组件挂载两次
4. 用 Preserve log 看路由切换是否重复拉

## 参考答案

### 操作步骤（照着点）

1. Network → Fetch/XHR → Clear → 勾选 **Preserve log**。
2. 进入会拉列表的页面（或切换路由再回来）。
3. 在列表里找 **同一 URL 连续两条**（Time 接近）。
4. 分别点开两条，看右侧 **Initiator**：
   - 点蓝色链接跳到 Sources 对应行（`fetch` / `axios.get` / 封装 `request`）。
5. 判断常见原因：
   1. **React 18 StrictMode（开发态）** 有意双调用 effect → 生产可能只有一次；别只在开发环境「修假问题」。
   2. **useEffect 依赖写错** 导致重复执行。
   3. 父组件重渲染导致子组件反复 mount。
   4. 路由守卫 / 全局拦截器里又调了一次。
6. 验证：在发请求函数第一行打 `console.count('fetchList')`，看次数是否与 Network 一致。
7. 修完再 Clear 走一遍，确认只剩业务需要的次数。

### 加分：看 Call Stack

部分请求 Initiator 旁可展开调用栈，能看到是生命周期还是事件处理函数触发。

## 可能追问

- 如何避免严格模式双请求打爆后端？→ 请求层做 in-flight 去重 / AbortController，生产仍有益。
- GraphQL 同路径不同 body 怎么辨认？→ 看 Payload 别只看 Name。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [接口请求怎么排查](04-接口请求怎么排查.md)
- [取消与断线重连](../03-AI前端/请求取消与断线重连.md)
- [项目：列表竞态](../09-项目深挖/D02-小程序列表竞态.md)
- [React 数据获取陷阱](../02-React/09-其他/在 React 中进行数据获取时，有哪些常见的陷阱？.md)
