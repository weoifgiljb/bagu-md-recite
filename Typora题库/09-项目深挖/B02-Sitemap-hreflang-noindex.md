# 题 8：Sitemap / hreflang / noindex 在静态多语言站怎么配合？

## 面试官可能怎么问

- Sitemap 收哪些 URL？
- hreflang 和 404 的关系？
- forceNoIndex 的页面还出 HTML 吗？

## 口述结构（90 秒）

1. Sitemap：indexable 且文件存在
2. hreflang：只列真实生成语言，不列 404
3. noindex：可出 HTML，但不收录、不进 Sitemap
4. llms.txt ≠ Google Sitemap；无 Search Console 不报涨幅

## 参考答案

### 对应问 1：Sitemap 收哪些 URL

规则：
1. 本次构建 **indexable**
2. 对应静态文件**真实存在**
3. `lastmod` 跟内容真实改动，**不要用构建时钟刷全站**

步骤：索引表 → 过滤 forceNoIndex → 检查文件 → 写 sitemap.xml（或按语言拆分）。

### 对应问 2：hreflang 和 404

- hreflang **只列本次真实生成的语言**
- **不列**会 404 的 URL
- `canonical` 指向自身；`hreflang` 的 href 必须与实际 HTML 路径一致（含 zh 无前缀）

错误示范：索引写了 pt，HTML 没生成，却在 hreflang 里挂 `/pt/...` → 搜索引擎信任下降。

### 对应问 3：forceNoIndex 还出 HTML 吗

**会出 HTML**（预览/内链可能仍要），但：
- meta robots = noindex
- **不进 Sitemap**
- OG：`og:url` = canonical；缺语言图可回退通用图，路径必须存在

**llms.txt**：给模型的站点目录，**不是**另一种 Google Sitemap；没有 Search Console 证据时，**别说收录提升 xx%**。


## 可能追问

- sitemap index 何时上？→ 多文件/多语言体量变大时。
- 预发域名进生产 Sitemap？→ 绝不；按环境隔离生成。
- 多 CDN 主备落地了吗？→ 未落地就说方案，不说已上线。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
