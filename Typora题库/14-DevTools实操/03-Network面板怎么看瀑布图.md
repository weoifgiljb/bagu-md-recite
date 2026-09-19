# 题 3：Network 面板怎么看？瀑布图每一段是什么意思？

## 面试官可能怎么问

- 瀑布图里 Waiting (TTFB) 和 Content Download 区别？
- 怎么找出「最慢的那条请求」？
- Initiator、Priority、Size 列怎么用？

## 口述结构（90 秒）

1. 打开 Network → Preserve log → Disable cache → 复现
2. 过滤 Fetch/XHR 或按域名
3. 瀑布：排队→连→SSL→TTFB→下载
4. 慢在服务端看 TTFB；慢在包体看 Download；慢在前端排队看 Queueing

## 参考答案

### 1. 推荐默认勾选

1. 打开 **Network**。
2. 勾选 **Preserve log**（跳转/刷新不丢历史）。
3. 勾选 **Disable cache**（避免「我改了代码怎么还是旧的」）。
4. 需要时把网络限速改成 Fast 3G 模拟弱网。
5. 点清除 → 再操作一遍页面，保证列表干净。

过滤：

- 顶栏 **Fetch/XHR**：只看接口。
- **JS / CSS / Img**：静态资源。
- 过滤框：域名、路径关键字，如 `api`、`sse`。

### 2. 瀑布图（Waterfall）各段含义

点开某条 → **Timing** 更准；列表里的色条是缩略：

1. **Queueing**：在浏览器队列里等（连接数限制、HTTP/1.1 同域并发有限等）。
2. **DNS Lookup**：域名解析（有缓存则很短或没有）。
3. **Initial connection / SSL**：TCP + TLS 握手。
4. **Request sent**：请求头/体发出去。
5. **Waiting (TTFB)**：等到首字节——多半是 **服务器处理 + 到你的链路**。接口「业务慢」常看这里。
6. **Content Download**：收响应体——包大、网慢会变长。

口诀：

- **TTFB 很长**：先怀疑后端/网关/冷启动/DB，不要先怪渲染。
- **Download 很长**：看 Size 是否巨大、是否未压缩、是否一次拉全量列表。
- **Queueing 很长**：同域并发打满、或主线程太忙拖慢网络回调（可和 Performance 对照）。

### 3. 列表列怎么读

- **Status**：200 / 304 / 401 / 404 / 500 / (failed) / CORS error。
- **Type**：xhr、fetch、eventsource、script…
- **Initiator**：谁发起的（JS 文件:行号，或 parser）。点进去能跳到发请求的代码。
- **Size**：括号里有时是「内存中的大小 vs 传输大小」；注意 memory cache / disk cache 标记。
- **Time**：总耗时；旁边瀑布条。
- **Priority**：浏览器调度优先级（最高/高/低）；关键接口被挤到低优时要心里有数。

### 4. 实操：找出最慢接口

1. 过滤 Fetch/XHR。
2. 点 **Time** 列排序（或看瀑布最靠右的）。
3. 点开 → Timing 看是 TTFB 还是 Download。
4. 看 Response 是否过大；Headers 里有没有 `Content-Encoding: gzip/br`。
5. Initiator 确认是不是重复请求（StrictMode/重复 useEffect）。

## 可能追问

- 304 和 200 from disk cache 区别？→ 304 是协商缓存「未改走缓存」；disk/memory cache 是直接命中不强校验（视策略而定）。
- HTTP/2 多路复用后 Queueing 还会严重吗？→ 同连接多路会缓解 HTTP/1 的队头阻塞，但仍可能受浏览器/服务器限流影响。

## 我的笔记

## 相关跳转

（Typora 可点；背诵本当索引）

- [强缓存与协商缓存](../07-浏览器网络补洞/04-强缓存与协商缓存.md)
- [CORS 与跨域](../07-浏览器网络补洞/05-CORS与跨域.md)
- [JS：优化网络请求](../01-JavaScript/12-性能优化/如何优化网络请求以获得更好的性能？.md)
- [实操：弱网与缓存](13-实操-弱网与缓存对比.md)
