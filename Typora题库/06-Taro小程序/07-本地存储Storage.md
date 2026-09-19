# 题 7：小程序本地存储怎么用？和 localStorage、缓存策略有何不同？

## 面试官可能怎么问

- Storage 容量和同步/异步 API 怎么选？
- 适合存什么？不适合存什么？
- 和请求缓存、内存态如何分层？

## 口述结构（90 秒）

1. Taro.setStorage / getStorage；同步 API 小心阻塞
2. 存 Token、草稿、最近筛选；不存大正文与密钥
3. 分层：内存 > Storage > 网络；设版本号与过期
4. 退出登录与隐私合规要清存储

## 参考答案

### 1. API 与限制

- 异步：`Taro.setStorage({ key, data })` / `getStorage` / `removeStorage` / `clearStorage`。  
- 同步：`setStorageSync` 等——**大数据或主线程热点慎用**，会卡住逻辑层。  
- 容量：单应用有上限（常见讨论约 10MB 量级，以平台文档为准）；单 key 也不宜塞巨对象。  
- 数据可 JSON 序列化；注意 Date、Map、循环引用。

```ts
await Taro.setStorage({ key: 'doc_filters', data: { status: 'pending', q: '' } })
const { data } = await Taro.getStorage({ key: 'doc_filters' })
```

### 2. 存什么 / 不存什么

| 适合 | 不适合 |
| --- | --- |
| access_token、用户偏好 | session_key、私钥 |
| 列表筛选条件、草稿 | 整库文档正文 |
| 最近会话 id | 无过期的大缓存随便堆 |

步骤：写之前估大小；读失败当未登录/无缓存；关键配置带 `version` 字段，结构升级时迁移或丢弃。

### 3. 与内存、网络缓存分层

1. **内存（全局 store）**：当前会话消息、进行中请求——最快，杀进程即无。  
2. **Storage**：跨启动需要的轻状态。  
3. **网络**：权威数据；Storage 只做 stale-while-revalidate。  

```ts
type CacheBox<T> = { v: number; expireAt: number; data: T }
function readCache<T>(key: string, v: number): T | null {
  try {
    const box = Taro.getStorageSync(key) as CacheBox<T>
    if (!box || box.v !== v || Date.now() > box.expireAt) return null
    return box.data
  } catch { return null }
}
```

**业务例子**：最近打开文档 id 列表进 Storage；AI 消息列表以内存为主，必要时只持久化 conversationId。退出登录 `removeStorage` 掉 Token 与个性化缓存。

### 4. 实践模式与坑

1. **键名加前缀**：`docreview:v1:token`，避免多小程序/多环境串数据。  
2. **版本迁移**：读到旧 version 直接丢弃或跑 `migrate()`，不要假设字段永不变。  
3. **并发写**：同一 key 避免多处 sync 写；集中到 storage 小模块。  
4. **隐私合规**：用户拒绝授权或注销账号时，清个人标识与草稿。  
5. **调试**：开发者工具 Storage 面板可清；真机要给「清除缓存」入口方便测试。  

对比 H5 `localStorage`：API 相似，但小程序有更明确的配额与异步优先建议；且 **不会随请求自动发送**，安全模型接近「手动保管的本地文件」，鉴权仍靠你每次塞 Header。

## 可能追问

- 和 Cookie 比？→ Storage 不自动跟请求走，需手动挂 Header。
- Storage 被用户清掉？→ 当作冷启动，走登录与首屏拉取。
- 加密存储？→ 可对敏感字段加密，但密钥仍在端上，只能提高门槛。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
