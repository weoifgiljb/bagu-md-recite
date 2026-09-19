# 题 7：Next 官网：SSG 多语言路由与中文无前缀怎么讲？

## 面试官可能怎么问

- URL 到静态 HTML 的链路？
- 中文为什么无前缀？
- 缺某个语言的 JSON 怎么办？

## 口述结构（90 秒）

1. Pages Router + SSG + 静态导出，CDN 吐 HTML
2. 中文无前缀；其他 /${locale}；/zh 应 404
3. 缺 JSON = 构建失败，不是英文静默兜底
4. ready ≠ indexable；个人边界勿夸大 owner

## 参考答案

### 对应问 1：URL → 静态 HTML

骨架：**Pages Router + SSG + 静态导出**，CDN 直接吐 HTML。

步骤：
1. URL 进入页面索引（哪些 path × locale 要生成）
2. `getStaticPaths` 枚举路径
3. `getStaticProps` 读对应 locale JSON
4. 构建导出静态 HTML/JSON；运行时不再打 CMS

### 对应问 2：中文为什么无前缀

产品要求默认中文更短：`/alternatives/...`（zh）与 `/pt/alternatives/...` 等。

实现要点：
- 两套薄路由共享 loader / View / SEO 组件
- `toPagePath`：`zh` → 无前缀；其他 → `/${locale}/...`
- **`/zh/...` 应 404**，避免重复 URL

### 对应问 3：缺某个语言的 JSON

**不是**默默英文兜底。

- 索引写了 `pt` 但文件缺失 → **应构建失败**（早暴露）
- 只想发 en → 索引先只 `ready` en
- `ready` ≠ `indexable`：能出 HTML 不等于进 Sitemap

**个人边界**：参与营销页与路由/Sitemap/OG/noindex 等；勿夸大成整站架构 owner。


## 可能追问

- hreflang 列哪些？→ 只列本次真实生成的语言（见 B02）。
- canonical？→ 指向自身规范 URL；zh 无前缀版。
- 为何不用 App Router SSR？→ 营销页静态优先、成本与缓存简单；按当时选型说。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
