# 题 11：transition 和 animation 区别？怎么用才不卡？

## 面试官可能怎么问

- 二者差在哪？什么时候用哪个？
- 哪些属性适合做动画？为什么少动画 `width/left`？
- `animation` 关键帧、`infinite`、逆向怎么写？
- 怎么排查动画卡顿？`will-change` 要不要加？

## 口述结构（90 秒）

1. `transition`：状态 A→B 的过渡，靠类名/伪类切换触发
2. `animation`：可多关键帧、可循环、不必有「两端状态」
3. 性能：优先 `transform`/`opacity`；布局属性易回流
4. 可访问：`prefers-reduced-motion` 减弱动画
5. 排查：Performance看是否 Layout；合成层是否过多

## 参考答案

### 1. 对比

| | transition | animation |
| --- | --- | --- |
| 触发 | 属性值变化 | 立刻按关键帧播放 |
| 关键帧 | 隐式两端 | `@keyframes` 多段 |
| 循环 | 一般一次 | `infinite` 等 |
| 典型 | hover、展开收起 | 加载转圈、入场秀 |

```css
.btn {
  transition: background-color .2s ease, transform .2s ease;
}
.btn:hover { transform: translateY(-1px); }

@keyframes spin {
  to { transform: rotate(360deg); }
}
.loader {
  animation: spin .8s linear infinite;
}
```

### 2. 常用写法细节

```css
.panel {
  transition-property: transform, opacity;
  transition-duration: .2s;
  transition-timing-function: ease;
  transition-delay: 0s;
}
/* 简写 */
.panel { transition: transform .2s ease, opacity .2s ease; }
```

```css
.toast {
  animation: toast-in .25s ease both; /* both=forwards+backwards 填模式 */
}
@keyframes toast-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

- `animation-fill-mode: forwards`：停在最后一帧样式。  
- 逆向/往返：`animation-direction: reverse | alternate | alternate-reverse`（如 loading 用 `alternate` 来回）。  
- 进出场两套动画可分别绑 `.is-enter` / `.is-leave`（Vue `<Transition>` 同理）。

### 3. 遇到问题怎么办

**问题 A：动画卡、掉帧**

1. Performance 录制：看有无每帧 Layout。  
2. 检查是否动画了 `top/left/width/height/margin`。  
3. 改成：

```css
/* 好 */
.drawer { transform: translateX(100%); transition: transform .2s; }
.drawer.open { transform: translateX(0); }

/* 差 */
.drawer { right: -300px; transition: right .2s; }
.drawer.open { right: 0; }
```

4. 减少同时动画的大面积滤镜/`box-shadow`。  
5. `will-change: transform` 仅在即将动画时加，结束后去掉，防内存涨。

**问题 B：transition 不播放**

1. 两端没有可插值差异（如 `display:none`↔`block` 不能平滑）。  
2. 处理：用 `opacity`+`visibility` 或 `max-height`（有副作用）或 JS 分两帧改类。  
3. 初次挂载：先插入默认类，下一帧再加 `.open`（`requestAnimationFrame` 两次）。

**问题 C：进场有、出场没**

- 元素已被移除 DOM。需延迟删除等动画 `animationend`/`transitionend`（框架 Transition 组件帮你做）。

**问题 D：无障碍**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**业务例子**：侧滑抽屉用 `transform`；骨架屏 shimmer 用 `transform` 位移动渐变；数字翻滚别每帧改 layout。

## 可能追问

- `ease`/`cubic-bezier`？→ 控制加速度；Material 常用标准曲线。  
- JS 动画库？→ 复杂时间轴可用；简单 UI 优先 CSS。  
- GPU 加速？→ 不是加了就快；错误提升层反而吃内存。

## 我的笔记

- 定义：
- 原理：
- 业务例子：
- 可能追问：
