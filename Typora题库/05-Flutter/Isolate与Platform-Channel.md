# 题：Isolate 与 Platform Channel 是什么？怎么用？

## 面试官可能怎么问

- Isolate 和普通线程/Web Worker 有何不同？
- 什么时候该开 Isolate？怎么传数据？
- Platform Channel 三种通道怎么选？注意什么坑？

## 口述结构（90 秒）

1. Isolate：独立堆与事件循环，无共享内存，靠消息传
2. CPU 重活（解析/编解码）放 Isolate，避免卡 UI isolate
3. Channel：Method / Event / BasicMessage；注意线程与类型
4. 大对象传穿过桥要控频率与拷贝成本

## 参考答案

### 对应问 1：Isolate 是什么

- Flutter/Dart：**每个 Isolate 有自己的堆与事件循环**，**不共享内存**
- 通信靠 **port 发消息**（复制或可转移的数据），不是随便共享对象
- 主 Isolate（UI）卡了 → 掉帧；所以重计算要挪走

对比：
- 像 Web Worker：消息通信、无共享 DOM/无共享堆
- 不像 Java 线程：不能直接共享可变对象加锁（Dart 模型不同）

### 对应问 2：何时开 Isolate、怎么传

**适合**：JSON 大包解析、图片编解码、加解密、本地报表聚合。  
**不适合**：每次按键都 `spawn`（启动贵）；极短任务直接主 isolate 更合适。

步骤（`compute` / `Isolate.run`）：
1. 把**可序列化**入参准备好（避免抓 UI 对象）
2. `final result = await Isolate.run(() => heavy(input));`
3. 回主 isolate 再 `setState` / 通知状态管理
4. 长时间任务用常驻 Isolate + SendPort，避免反复 spawn

### 对应问 3：Platform Channel

| 类型 | 用途 |
| --- | --- |
| **MethodChannel** | 一次请求-响应（调原生 API） |
| **EventChannel** | 原生 → Dart 事件流（传感器、进度） |
| **BasicMessageChannel** | 双向消息，自定义 codec |

步骤（MethodChannel）：
1. Dart：`channel.invokeMethod('getBattery')`
2. Android/iOS：注册 handler，回结果或 `result.error`
3. Dart 用 `try/catch` 处理 `PlatformException`

**坑**：
- 必须在正确线程回传结果（尤其 Android）
- 类型要走 StandardMessageCodec 支持的集合；复杂对象自己编码
- 高频大数据走桥 → 卡顿；考虑压缩、批处理、或文件路径传递
- 热重启后原生侧监听是否还在要心里有数

**业务例子**：读安全存储/蓝牙/文件选图用 MethodChannel；下载进度用 EventChannel；大日志解析用 Isolate。


## 可能追问

- Isolate 能调 Platform Channel 吗？→ 通常在主 isolate 调桥；后台 isolate 以算力为主。
- FlutterIsolate 插件？→ 简化常驻 isolate；开口说清依赖。
- 和 compute 区别？→ compute 是封装好的一次性 isolate 任务。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
