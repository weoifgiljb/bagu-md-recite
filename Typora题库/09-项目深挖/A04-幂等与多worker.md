# 题 4：如何保证同一 key 不被重复处理？多 worker 怎么设计？

## 面试官可能怎么问

- 当时落地的是什么？
- 如果补多 worker / 重启，你怎么设计？
- 幂等键怎么组成？

## 口述结构（90 秒）

1. 先分层：当前实现 vs 改进设计
2. 当前：进程内 bool + CMS 版本号
3. 改进：幂等键 UNIQUE + 状态机 + lease + outbox
4. 九字段任务表只作「若补多 worker」口述

## 参考答案

### 对应问 1：当时落地的是什么

**当前实现（必须先说）**
- 进程内「处理中」bool + CMS **版本号**防重入
- 承认：**单进程假设**；进程崩溃/多实例会不够

开口：「当时落地的是进程内状态 + CMS 版本；够支撑当时吞吐。」

### 对应问 2：若补多 worker / 重启

**改进设计（前缀固定：「如果补多 worker…」）**

1. **入队幂等**：`idempotency_key` UNIQUE，`INSERT … DO NOTHING`
2. **状态机**：`PENDING → CLAIMED → RUNNING → SUCCEEDED / FAILED / COMPENSATING`
3. **lease**：认领时写 `lease_expire_at`；超时回收，避免死锁
4. **outbox**：翻译完成与 CMS 同步解耦；同步失败只重试 outbox，不重跑翻译（除非策略要求）

**不要**把任务表说成已经上线。

### 对应问 3：幂等键怎么组成

推荐：`locale + i18n_key + content_hash`  
- 源文变更 → `content_hash` 变 → 可合法再译  
- 同内容重复投递 → UNIQUE 挡住

**九字段（改进口述）**：`task_id` / `idempotency_key` / `record_id` / `locale` / `content_hash` / `status` / `lease_expire_at` / `retry_count` / `policy_version`

步骤（认领）：
1. 事务内选 PENDING 且 lease 空/过期
2. 写 CLAIMED + 新 lease
3. 跑翻译；成功写 SUCCEEDED + outbox；失败按可重试策略递增 `retry_count`


## 可能追问

- lease 超时怎么避免双写？→ 写 CMS 前再校验 lease/version；outbox 幂等消费。
- content_hash 源文变更？→ 新 hash 新任务；旧 SUCCEEDED 可归档。
- COMPENSATING 场景？→ 已写半边需回滚/对账时进入补偿态。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
